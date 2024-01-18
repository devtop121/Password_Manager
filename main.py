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
            pathfile = os.path.join(directory, r"path.txt")
            os.mkdir(directory)
            print("Created directory at", directory)
            #write to this path.txt the path for further use.
            with open(pathfile, 'w') as file:
                file.write(pathfile)
            dbinit.init_db(db_path)
        #No skips the folder creation, not sure how to move forward yet.    
        elif installinit.lower() == 'no':
            login.handle_login()            
        else:
            initialize()
    initialize()




