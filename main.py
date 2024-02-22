import os, sys, stat
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
import dbinit
import login
import subprocess
import re

def get_version():
    return "1.2"

def register():
    global db_path
    pathdb = "C:/pwpath/path.txt"
    try:
        with open(pathdb, 'r') as file:
            content1 = file.read()
            login.new_user(content1)
    except Exception as e:
        print("An error occurred, you most likely are yet to install the program. Install it before creating new users.")

def login_menu(db_path):

    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f'{width}x{height}+{x}+{y}')
    
    
    def on_enter_pressed(event=None):
        login_button.invoke()  # Trigger the button click

    window = tk.Tk()
    window.title("Login Menu")

    window_width = 340
    window_height = 440

    center_window(window, window_width, window_height)

    #Creating widgets
    login_label = tk.Label(window, text=f"Welcome! pwmanager version: {get_version()}")
    username_label = tk.Label(window, text="Username")
    username_entry = tk.Entry(window)
    password_entry = tk.Entry(window, show="*")
    password_label = tk.Label(window, text="Password")
    username_entry.focus_set()
    #Fetching input data
    def fetch():
        user = username_entry.get()
        password = password_entry.get()
        if password == "" or user == "":
            return
        return login.handle_login(db_path,user,password, window)
    login_button = tk.Button(window, text="Login", command=fetch)

    #Placing wdigets on the screen
    login_label.grid(row=0, column=0, columnspan=2)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    login_button.grid(row=3, column=0, columnspan=2)
    window.bind("<Return>", on_enter_pressed)

    window.mainloop()


def validate_password_main(user, password):
        if len(password) < 12:
            print("Password invalid. It should be atleast 12 characters and include uppercase, special character and a number.")
            return None, None
        res = bool(re.search(r'[A-Z]', password) and bool(re.search(r'\d', password) and bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))))
        if res == True:
            print("Correct password format")
            return user, password
        else:
            print("password invalid")
            return None, None

def install_program():
    def install_cryptography():
            try:
                python_command = sys.executable
                install_command = [python_command, "-m", "pip", "install", "cryptography"]
                subprocess.run(install_command, check=True)
                print("Select a folder for install")
            except subprocess.CalledProcessError as e:
                print(f"Error installing encryption method: {e}")

    def get_values():
        user = username_entry.get()
        password = password_entry.get()
        repassword = repassword_entry.get()
        if password == repassword:
            user, password = validate_password_main(user, password)
            if user and password:
                install_cryptography()
                root = tk.Tk()
                root.withdraw()
                #User chooses a path
                path = askdirectory(title='Select Folder')
                #To this user chosen path we append our main file directory "pwmanager1.0"
                directory = os.path.join(path, r"pwmanager1.0")
                db_path = os.path.join(directory, r"sqlite.db")
                #we create a path file inside directory pwmanager. Not sure yet if this is even useful
                pathfile = "C:/pwpath/path.txt"
                os.mkdir(directory)
                os.mkdir("C:/pwpath/")
                print("Created directory at", directory)
                #write to this path.txt the path for further use.
                with open(pathfile, 'w') as file:
                    file.write(db_path)
                dbinit.init_db(db_path, user, password)
                window.destroy()
                root.destroy()
                login_menu(db_path)
        else:
            print("Passwords didn't match.")

    window = tk.Tk()
    window.title(f"Pwmanager{get_version()} installer")
    window.geometry('340x440')
    username_label = tk.Label(window, text="Username")
    username_entry = tk.Entry(window)
    password_entry = tk.Entry(window, show="*")
    password_label = tk.Label(window, text="Password")
    repassword_label = tk.Label(window, text="Confirm password")
    repassword_entry = tk.Entry(window, show="*")
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    repassword_label.grid(row=3, column=0)
    repassword_entry.grid(row=3, column=1)
    create_button = tk.Button(window, text="Create user", command=get_values)
    create_button.grid(row=4, column=0, columnspan=2)
    window.mainloop()

def program_installed():
    path = "C:\\pwpath\\path.txt"
    if os.path.exists(path):
        with open(path, 'r') as file:            
            db_path = file.read()
            login_menu(db_path)
    else:
        return install_program()

if __name__ == "__main__":    
    program_installed()


#gets a value after initialize is finished.
#db_path = None
#if main.py is ran directly as a script, not from other scripts as an import





