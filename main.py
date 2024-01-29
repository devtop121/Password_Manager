import os, sys, stat
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
import dbinit
import login
import subprocess
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
                    print("Encryption method installed successfully")
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




