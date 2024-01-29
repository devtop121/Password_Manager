import sqlite3
from sqlite3 import Error
from pathlib import Path
import hashlib
import secrets
import getpass
import login
import os
import main_menu

# function which updates database with the values from insert data window
def add_data(db_path,user, website, username, password):
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
    except Exception as e:
        print(e)
        return
    if len(website) == 0 and len(username) == 0 and len(password) == 0:
        return
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT salt FROM user_auth WHERE user = ?", (user,))
        salt = c.fetchone()
        salt = salt[0]

        insert_passwords = "INSERT INTO passwords (user, website, username, password) VALUES (?,?,?,?)"
        c.execute(insert_passwords, (user,website,username, password))
        conn.commit()
        print("Added data successfully.")
    except Exception as e:
        print(e)
    finally:
        conn.close()
        main_menu.update_interface(db_path, user)
# function for removing inserted data.
def remove_data():
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import padding
    except Exception as e:
        print(e)
    print("removing data")
