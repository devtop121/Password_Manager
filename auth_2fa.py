import pyotp
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from io import BytesIO
import tkinter as tk

def initialize_2fa(user, salt):
    load_dotenv()
    salt = salt[0]
    salt = salt.encode('utf-8')
    key = os.getenv('key')
    key = key.encode('utf-8')
    secret = pyotp.random_base32()
    combined_key = key + salt
    crypter = Fernet(combined_key)
    encrypted_secret = crypter.encrypt(secret.encode('utf-8'))
    decrypted_secret = crypter.decrypt(encrypted_secret).decode('utf-8')
    return encrypted_secret, secret

def decrypt_secret(secret, salt):
    load_dotenv()
    salt = salt[0]
    salt = salt.encode('utf-8')
    key = os.getenv('key')
    key = key.encode('utf-8')
    combined_key = key + salt
    crypter = Fernet(combined_key)
    decrypted_secret = crypter.decrypt(secret).decode('utf-8')
    totp = pyotp.TOTP(decrypted_secret)
    return totp.now()
    
    


