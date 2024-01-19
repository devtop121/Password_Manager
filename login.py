import getpass
import sqlite3
import hashlib
import secrets
import login
import main_menu
#function for checking user and password from auth_user table in database.
def handle_login(db_path):
    user = input("Username: ")
    password = getpass.getpass("Password: ")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM user_auth WHERE user = ?", (user,))
    result = c.fetchone()
    if result:
        password = password + result[2]
        password = hashlib.sha256(password.encode()).hexdigest()
        if password == result[1]:
            main_menu.mainmenu(user)
    else:
        print(f"No user named {user}")
    conn.close()