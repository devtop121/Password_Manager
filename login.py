import getpass
import sqlite3
#function for checking user and password from auth_user table in database.
def handle_login(db_path):
    user = input("Username: ")
    password = getpass.getpass("Password: ")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM user_auth WHERE USER = ?", (user,))
    result = c.fetchone()
    if result:
        print(f"found the user {user}")
    else:
        print("didnt find anything")
    conn.close()