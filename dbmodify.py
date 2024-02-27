import sqlite3
import hashlib
import os
import main_menu
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from tkinter import messagebox
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# function which updates database with the values from insert data window
def add_data(db_path, user, website, username, password):
    if len(website) == 0 and len(username) == 0 and len(password) == 0:
        return
    config_file_path = resource_path('common_passwords.txt')
    with open(config_file_path, 'r') as file:
        # Read all lines in the file
        file_contents = file.readlines()
    file_contents = [line.strip() for line in file_contents]
    if password in file_contents:
        insert = messagebox.askyesno("Weak password","The password is in a list of common passwords. Using this password negates any use of a password manager. Proceed?")
        if insert == False:
            return
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT salt FROM user_auth WHERE user = ?", (user,))
        salt = c.fetchone()
        salt = salt[0]
        salted_string = password + salt
        salt = salt.encode('utf-8')
        load_dotenv()
        key = os.getenv('key')
        key = key.encode('utf-8')
        combined_key = key + salt
        crypter = Fernet(combined_key)
        pw = crypter.encrypt(password.encode('utf-8'))
        hashed_password = hashlib.sha256(salted_string.encode('utf-8')).hexdigest()
        insert_passwords = "INSERT INTO passwords (user, website, username, password, hashed_password) VALUES (?,?,?,?,?)"
        c.execute(insert_passwords, (user,website,username,pw,hashed_password))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        main_menu.update_interface(db_path, user, crypter)
