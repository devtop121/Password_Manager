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
def init_db(db_path):
    conn = None
    #initialize 2 tables: user_auth and passwords.
    try:
        init_users = """ CREATE TABLE IF NOT EXISTS user_auth (
                                        user TEXT PRIMARY KEY,
                                        password TEXT NOT NULL,
                                        salt TEXT NOT NULL
                                    ); """
        init_table = """ CREATE TABLE IF NOT EXISTS passwords (
                                        id INTEGER PRIMARY KEY,
                                        user TEXT NOT NULL,
                                        website TEXT,
                                        username TEXT,
                                        password BLOB,
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
        user = input("Enter a username: ")

        #function for making double checking your password. if they dont match it calls the function again.
        def password_create():
            password = getpass.getpass("Enter a password: ")
            re_password = getpass.getpass("Enter password again: ")
            if password != re_password:
                print("Passwords didn't match.")
                return password_create()
            else:
                print("Password created.")
                return password
        
            
        combined_password = password_create() + salt
        hashed_password = hashlib.sha256(combined_password.encode()).hexdigest()
        insert_auth = "INSERT INTO user_auth (user, password, salt) VALUES (?,?,?)"
        #add user to users with name, hashed password and unique salt. i used cryptographic hashing instead of password hashing.
        #this is debatable but in this case it didnt require downloading bcrypt or something else.
        c.execute(insert_auth, (user, hashed_password, salt))
        #commit saves changes.
        conn.commit()
        print("Database successfully created.")
        want_to_login = input("Do you want to login? Yes or No ")
        if want_to_login.lower() == 'yes':
            pathdb = "C:/pwpath/path.txt"
            with open(pathdb, 'r') as file:
                path = file.read()
                #call login_handle with path of database.
                login.handle_login(path)
        if want_to_login.lower() == 'no':
            pass
    #incase of error it prints the error e which is determined by error library.
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        


