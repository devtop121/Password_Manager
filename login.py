import getpass
import sqlite3
import hashlib
import secrets
import login
import main_menu
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