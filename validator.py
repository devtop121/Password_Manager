import re
import login

def validate_password(user, password, db_path):
        if len(password) < 12:
            return
        res = bool(re.search(r'[A-Z]', password) and bool(re.search(r'\d', password) and bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))))
        if res == True:
            login.insert_user(user, password, db_path)
        else:
            return