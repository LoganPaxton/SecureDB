import os
import supabase
from cryptography.fernet import Fernet
import uuid
from random import randint

# Initialize Supabase client
key = os.environ.get("KEY")
url = os.environ.get("URL")
if not key or not url:
    raise ValueError("Supabase credentials are missing.")
client = supabase.create_client(url, key)

# Generate Fernet key
f = Fernet(Fernet.generate_key())


def gen_charset(char=""):
    charset = ""
    for _ in range(len(char)):
        index = randint(0, len(char) - 1)
        charset += char[index]
    return charset


def gen_api_key(charset=""):
    data = charset.encode()  # Encode charset to bytes
    encrypted_data = f.encrypt(data)
    encrypted_key = encrypted_data.decode()  # Decode bytes to string
    encrypted_key = encrypted_key.replace("b'", "").replace("'", "")
    return encrypted_key


def handle_login(key=""):
  response = client.from_('UUIDs').select('id').eq('id', key).execute()
  if response.get('error'):
    print("Error:", response['error'])
    return None
  data = response.get('data')
  if data:
    return data[0]['id']
  return None




def handle_signup():
    uuid_key = str(uuid.uuid4())
    print("Your UUID: ", uuid_key)
    print("You will use this to log into SecureDB.")
    print("Do NOT lose this or share this key!")
    input("If you agree, press enter.")
    data, count = client.table("UUIDs").insert({"id": uuid_key}).execute()
    print("Signup successful. You can now log in.")


print("Hello, welcome to the API key generator!")
print("This will be used for SecureDB.")
print("--Options--")
print("1. Sign Up\n2. Sign In\n3. Generate API Key")
opt = input(">> ")
if opt == "1":
    handle_signup()
elif opt == "2":
    print("Please enter your key")
    ukey = input(">> ")
    user_id = handle_login(ukey)
    if user_id:
        print("Login successful. User ID:", user_id)
    else:
        print("Invalid UUID. Please try again.")
elif opt == "3":
    print("Sorry! Generating an API Key is not available at this time!")
else:
    print("Please enter a valid option!")
