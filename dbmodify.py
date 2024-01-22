import sqlite3
from sqlite3 import Error
from pathlib import Path
import hashlib
import secrets
import getpass
import login
# function which runs with the values from insert data window
def add_data(db_path, user, website, username, password):
    if len(website) == 0 and len(username) == 0 and len(password) == 0:
        return
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT salt FROM user_auth WHERE user = ?", (user,))
        salt = c.fetchone()
    except Exception as e:
        print(e)
    try:
        insert_passwords = "INSERT INTO passwords (user, website, username, password) VALUES (?,?,?,?)"
        c.execute(insert_passwords, (user,website,username,password))
        conn.commit()
        print("Added data successfully.")
    except Exception as e:
        print("Something went wrong")
    finally:
        if not conn.closed:
            conn.close()
# function for removing inserted data.
def remove_data():
    print("removing data")