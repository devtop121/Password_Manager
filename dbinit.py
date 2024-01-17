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
    try:
        init_table = """ CREATE TABLE IF NOT EXISTS passwords (
                                        id integer PRIMARY KEY,
                                        website text NOT NULL,
                                        password text
                                    ); """
        init_salt = """ CREATE TABLE IF NOT EXISTS salt (
                                        id integer PRIMARY KEY,
                                        user_salt text NOT NULL
                                    ); """
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(init_table)
        c.execute(init_salt)
        salt = secrets.token_hex(16) #16-byte (32 characters) hex salt
        insert_salt = "INSERT INTO salt (user_salt) VALUES (?)"
        c.execute(insert_salt, (salt,))
        conn.commit()
        print("Database successfully created.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        


