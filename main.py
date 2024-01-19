import os, sys, stat
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
import dbinit
import login
#gets a value after initialize is finished.
db_path = None
#if main.py is ran directly as a script, not from other scripts as an import
if __name__ == "__main__":
    #ask for install or login, Tkinter could be used for a proper installation gui
    def initialize():
        global db_path
        installinit = input("Yes for a new install, No for logging in: ")
        #Yes initializes the folders, tkinter is used for simple UI
        if installinit.lower() == 'yes':
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
        elif installinit.lower() == 'no':
            pathdb = "C:/pwpath/path.txt"
            #Try to find the path for database. if it fails to find it it means you have not installed the program.
            try:
                with open(pathdb, 'r') as file:
                    content = file.read()
                    login.handle_login(content)
            except Exception as e:
                print("An error occurred, maybe the link to your database has been cut or you have yet to install the program.")
        else:
            initialize()
    initialize()




