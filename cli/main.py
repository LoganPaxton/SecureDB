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

# Initialize logged_in variable
logged_in = False

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
    global logged_in  # Declare global variable
    response = client.from_('UUIDs').select('id').eq('id', key).execute()
    data = response.data
    try:
        assert data and len(data) > 0
        print("Logged in successfully!")
        logged_in = True  # Update logged_in to True after successful login
        global uid
        uid = data[0]['id']
        return True  # Return True if login is successful
    except AssertionError:
        print("Invalid UUID. Please try again.")
        return False  # Return False if login fails


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
print("1. Sign Up\n2. Sign In\n3. Generate API Key\n4. Exit")


while True:
    opt = input(">> ")

    if opt == "1":
        handle_signup()
    elif opt == "2":
        print("Please enter your key")
        ukey = input(">> ")
        handle_login(ukey)
    elif opt == "3":
        if logged_in:
            response = client.from_('UUIDs').select('api_key').eq('id', uid).execute()
            data = response.data
            if data and len(data) > 0:  # Check if API key already exists
                api_key = data[0]['api_key']
                if api_key:
                    print("An API key has already been generated for you:", api_key)
                else:
                    print("No API key found for your account. Generating a new one...")
                    charset = gen_charset()  # Generate charset
                    api_key = gen_api_key(charset)  # Generate API key using charset
                    data, count = client.table('UUIDs').update({
                        "api_key": api_key
                    }).eq('id', uid).execute()  # Update user's API key in the database
                    print("API key generated successfully:", api_key)  # Print generated API key
            else:
                print("No API key found for your account. Generating a new one...")
                charset = gen_charset()  # Generate charset
                api_key = gen_api_key(charset)  # Generate API key using charset
                data, count = client.table('UUIDs').update({
                    "api_key": api_key
                }).eq('id', uid).execute()  # Update user's API key in the database
                print("API key generated successfully:", api_key)  # Print generated API key
        else:
            print("Please log in first!")  # Inform user to log in before generating API key
    
    elif opt == "4":
        print("Goodbye!")
        break
    else:
        print("Please enter a valid option!")
