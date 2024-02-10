import os, sys, stat
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
import dbinit
import login
import subprocess

window = tk.Tk()
window.title("Login")
window.geometry('340x440')

#db_path = "C:\\pwmanager1.0\\sqlite.db"
#db_path = "H:/Password_manager\pwmanager1.0\sqlite.db"

#Creating widgets
login_label = tk.Label(window, text="Login")
username_label = tk.Label(window, text="Username")
username_entry = tk.Entry(window)
password_entry = tk.Entry(window, show="*")
password_label = tk.Label(window, text="Password")
#Fetching input data
def fetch():
    user = username_entry.get()
    password = password_entry.get()
    window.destroy()
    return login.handle_login(db_path,user,password)
login_button = tk.Button(window, text="Login", command=fetch) 

#Placing wdigets on the screen
login_label.grid(row=0, column=0, columnspan=2)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan=2)

window.mainloop()

#gets a value after initialize is finished.
db_path = None
#if main.py is ran directly as a script, not from other scripts as an import
if __name__ == "__main__":
    def initialize():
        global db_path
        installinit = input("Install for a new install, Login for logging in, Register for a new user: ")
        #Yes initializes the folders, tkinter is used for simple UI
        if installinit.lower() == 'install':
            #Function that installs encryption and decryption, planning to use AES
            def install_cryptography():
                try:
                    python_command = sys.executable
                    install_command = [python_command, "-m", "pip", "install", "cryptography"]
                    subprocess.run(install_command, check=True)
                    print("Select a folder for install")
                except subprocess.CalledProcessError as e:
                    print(f"Error installing encryption method: {e}")
            install_cryptography()
            #root is used to hide a small window tkinter puts up as default.
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
            dbinit.init_db(db_path)
        #No skips the folder creation, it calls login.py's handle_login function with the path inside path.txt
        elif installinit.lower() == 'login':
            pathdb = "C:/pwpath/path.txt"
            #Try to find the path for database. if it fails to find it it means you have not installed the program.
            try:
                with open(pathdb, 'r') as file:
                    content = file.read()
                    login.handle_login(content)
            except Exception as e:
                print("An error occurred, maybe the link to your database has been cut or you have yet to install the program.")
        elif installinit.lower() == 'register':
            pathdb = "C:/pwpath/path.txt"
            try:
                with open(pathdb, 'r') as file:
                    content1 = file.read()
                    login.new_user(content1)
            except Exception as e:
                print("An error occurred, you most likely are yet to install the program. Install it before creating new users.")
        else:
            initialize()
    initialize()



