import pyotp
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def initialize_2fa(user, salt):
    dotenv_path = resource_path('.env')
    load_dotenv(dotenv_path)
    salt = salt[0]
    salt = salt.encode('utf-8')
    key = os.getenv('key')
    key = key.encode('utf-8')
    secret = pyotp.random_base32()
    combined_key = key + salt
    crypter = Fernet(combined_key)
    encrypted_secret = crypter.encrypt(secret.encode('utf-8'))
    #decrypted_secret = crypter.decrypt(encrypted_secret).decode('utf-8')
    return encrypted_secret, secret

def decrypt_secret(secret, salt):
    dotenv_path = resource_path('.env')
    load_dotenv(dotenv_path)
    salt = salt[0]
    salt = salt.encode('utf-8')
    key = os.getenv('key')
    key = key.encode('utf-8')
    combined_key = key + salt
    crypter = Fernet(combined_key)
    decrypted_secret = crypter.decrypt(secret).decode('utf-8')
    totp = pyotp.TOTP(decrypted_secret)
    return totp.now()
    
    


