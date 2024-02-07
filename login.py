import getpass
import sqlite3
import hashlib
import secrets
import login
import main_menu
from pathlib import Path
import re
#function for checking user and password from auth_user table in database.
def handle_login(db_path):
    user = input("Username: ")
    user = user.strip()
    password = getpass.getpass("Password: ")
    password = password.strip()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    #takes the whole row where user is in database
    c.execute("SELECT * FROM user_auth WHERE user = ?", (user,))
    #takes the first result (row) but since primary key is user there should only be 1 row that matches.
    result = c.fetchone()
    #if result is true (it matched something)
    if result:
        #add password and salt together 
        password = password + result[2]
        #hash it and compare
        password = hashlib.sha256(password.encode()).hexdigest()
        if password == result[1]:
            conn.close()
            main_menu.mainmenu(user, db_path)
        else:
            print(f"Incorrect username or password")
    else:
        print(f"Incorrect username or password")
    conn.close()

def new_user(db_path):
            user = input("Enter a username: ")
            password = getpass.getpass("Enter a password: ")
            re_password = getpass.getpass("Enter password again: ")
            if password != re_password:
                print("Passwords didn't match.")
                return new_user(db_path)
            else:
                validate_password(user, password, db_path)

def retype_password(db_path, user):
            password = getpass.getpass("Enter a password: ")
            re_password = getpass.getpass("Enter password again: ")
            if password != re_password:
                print("Passwords didn't match.")
                return new_user(db_path)
            else:
                validate_password(user, password, db_path)

def validate_password(user, password, db_path):
        if len(password) < 12:
            print("Password invalid. It should be atleast 12 characters and include uppercase, special character and a number.")
            new_user(db_path)
        res = bool(re.search(r'[A-Z]', password) and bool(re.search(r'\d', password) and bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))))
        if res == True:
            insert_user(user, password, db_path)
        else:
            print("Password invalid. It should be atleast 12 characters and include uppercase, special character and a number.")
            retype_password(db_path, user)

def insert_user(user, password, db_path):
     try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        salt = secrets.token_hex(16)
        combined_password = password + salt
        hashed_password = hashlib.sha256(combined_password.encode()).hexdigest()

        insert_auth = "INSERT INTO user_auth (user, password, salt) VALUES (?,?,?)"
        #add user to users with name, hashed password and unique salt. i used cryptographic hashing instead of password hashing.
        #this is debatable but in this case it didnt require downloading bcrypt or something else.
        c.execute(insert_auth, (user, hashed_password, salt))
        # commit saves changes.
        conn.commit()
        print("User successfully created.")
     except sqlite3.Error as e:
            error_message = str(e)
            if "UNIQUE constraint failed: user_auth.user" in error_message:
                print("User already exists.")
            else:
                print(error_message)