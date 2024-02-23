import sqlite3
from sqlite3 import Error
from pathlib import Path
import hashlib
import secrets
import getpass
import login
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


#Initialize database, using SQLite.
def init_db(db_path, user, password):
    conn = None
    #initialize 2 tables: user_auth and passwords.
    try:
        init_users = """ CREATE TABLE IF NOT EXISTS user_auth (
                                        user TEXT PRIMARY KEY,
                                        password TEXT NOT NULL,
                                        salt TEXT NOT NULL,
                                        secret TEXT
                                    ); """
        init_table = """ CREATE TABLE IF NOT EXISTS passwords (
                                        id INTEGER PRIMARY KEY,
                                        user TEXT NOT NULL,
                                        website TEXT,
                                        username TEXT,
                                        password BLOB,
                                        hashed_password TEXT,
                                        FOREIGN KEY (user) REFERENCES user_auth (user)
                                    ); """
        #opens a connection and stores it in conn
        conn = sqlite3.connect(db_path)
        #cursor allows us to use commands such as insert etc...
        c = conn.cursor()
        #create 2 tables (all users and users stored passwords)
        c.execute(init_table)
        c.execute(init_users)
        #generate a salt that is different for each database(user)
        salt = secrets.token_hex(16) #16-byte (32 characters) hex salt
        #function for making double checking your password. if they dont match it calls the function again.
        combined_password = password + salt
        hashed_password = hashlib.sha256(combined_password.encode()).hexdigest()
        insert_auth = "INSERT INTO user_auth (user, password, salt) VALUES (?,?,?)"
        #add user to users with name, hashed password and unique salt. i used cryptographic hashing instead of password hashing.
        #this is debatable but in this case it didnt require downloading bcrypt or something else.
        c.execute(insert_auth, (user, hashed_password, salt))
        #commit saves changes.
        conn.commit()
    #incase of error it prints the error e which is determined by error library.
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        


