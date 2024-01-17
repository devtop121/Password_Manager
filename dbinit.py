import sqlite3
from sqlite3 import Error
import os, sys, stat
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
import hashlib
import secrets


#Initialize database, using SQLite.
def init_db(db_path):
    conn = None
    #initialize 2 tables: user_auth and passwords.
    try:
        init_users = """ CREATE TABLE IF NOT EXISTS user_auth (
                                        id integer PRIMARY KEY,
                                        user text NOT NULL,
                                        password text NOT NULL,
                                        salt text NOT NULL
                                    ); """
        init_table = """ CREATE TABLE IF NOT EXISTS passwords (
                                        id integer PRIMARY KEY,
                                        user_id INTEGER,
                                        website text,
                                        password text,
                                        FOREIGN KEY (user_id) REFERENCES user_auth (id)
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
        password = input("Enter a password: ")
        combined_password = password + salt
        hashed_password = hashlib.sha256(combined_password.encode()).hexdigest()
        insert_auth = "INSERT INTO user_auth (user, password, salt) VALUES (?,?,?)"
        #add user to users with name, hashed password and unique salt. i used cryptographic hashing instead of password hashing.
        #this is debatable but in this case it didnt require downloading bcrypt or something else.
        c.execute(insert_auth, (user, hashed_password, salt))
        #commit saves changes.
        conn.commit()
        print("Database successfully created.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        


