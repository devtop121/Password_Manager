import re
import login
from tkinter import messagebox
def validate_password(user, password, db_path):
        if len(password) < 12:
            return messagebox.showwarning("Invalid input.", "Make sure the password is atleast 12 characters long, contains uppercase and special characters.")
        res = bool(re.search(r'[A-Z]', password) and bool(re.search(r'\d', password) and bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))))
        if res == True:
            login.insert_user(user, password, db_path)
        else:
            return messagebox.showwarning("Invalid input.", "Make sure the password is atleast 12 characters long, contains uppercase and special characters.")