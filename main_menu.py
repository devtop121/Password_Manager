import sys
import sqlite3
import getpass
import hashlib
from tkinter import *
import tkinter.ttk as ttk
#rows contains the database for said user
def populate_treeview(tree, rows):
    for row in rows:
        tree.insert("", "end", values=row)
def mainmenu(user, db_path):
    # Shut down program once you close the window
    def on_closing():
        root.destroy()
        sys.exit()

    # Create main window
    root = Tk()
    root.geometry("800x600")
    frame = Frame(root)
    frame.pack()

    # Welcome text
    root.resizable(False, False)
    label = Label(frame, text=f"Hello {user}")
    label.pack()

    # Call function on_closing after exiting window
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Title of the window
    root.title("Password Manager 1.0")

    # Add 2 windows for switching menus
    notebook = ttk.Notebook(root)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    frame3 = ttk.Frame(notebook)
    #connect to the database to get users information
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM passwords WHERE user = ?", (user,))
    rows = c.fetchall()
    conn.close()

    # Add widgets to frame1
    label1 = Label(frame1, text=f"Look at all these passwords!")
    label1.pack()
    #Not too sure why first service doesnt work, but add 3 buttons which work.
    tree = ttk.Treeview(frame2, columns=("Service", "Username", "Password"), show="headings", height=20)
    tree.heading("#0", text="Service")
    tree.heading("#1", text="Service")
    tree.heading("#2", text="Username")
    tree.heading("#3", text="Password")
    #center text 
    tree.column("#0", anchor="center")
    tree.column("#1", anchor="center")
    tree.column("#2", anchor="center")
    tree.column("#3", anchor="center")

    y_scrollbar = Scrollbar(frame2, orient="vertical", command=tree.yview)
    y_scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=y_scrollbar.set)
    populate_treeview(tree, rows)

    tree.pack()

    # Add widgets to frame2
    label2 = Label(frame2, text=f"Modify your passwords here.")
    label2.pack()

    # Add widgets to frame2
    label3 = Label(frame3, text="2 Engineers and a hunger for perfected password manager.")
    label3.pack()
    notebook.add(frame1, text="Passwords")
    notebook.add(frame2, text="Add/remove passwords")
    notebook.add(frame3, text="About us")

    # Render the menus
    notebook.pack(fill=BOTH, expand=True)

    root.mainloop()

