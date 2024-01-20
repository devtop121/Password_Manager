import sys
import sqlite3
import getpass
import hashlib
from tkinter import *
import tkinter.ttk as ttk
from tkinter import simpledialog
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

    def insert_data():
    # Function to handle the insertion of data
        def handle_insert():
            # Get values from entry widgets
            service = service_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            # Close the input window
            input_window.destroy()
            

        # Create a new window for user input
        input_window = Toplevel(frame2)
        input_window.title("Insert Data")
        input_window.geometry("400x300")
        # Calculate the position to center the window on the screen
        # Center the window on the screen
        input_window.update_idletasks()
        width = input_window.winfo_width()
        height = input_window.winfo_height()
        x_position = (input_window.winfo_screenwidth() - width) // 2
        y_position = (input_window.winfo_screenheight() - height) // 2

        input_window.geometry(f"+{x_position}+{y_position}")

        # Entry widgets for user input
        service_label = Label(input_window, text="Service:")
        service_label.pack()
        service_entry = Entry(input_window)
        service_entry.pack()

        username_label = Label(input_window, text="Username:")
        username_label.pack()
        username_entry = Entry(input_window)
        username_entry.pack()

        password_label = Label(input_window, text="Password:")
        password_label.pack()
        password_entry = Entry(input_window, show="*")  # Use show="*" to hide the password
        password_entry.pack()

        # Button to confirm and insert data
        confirm_button = Button(input_window, text="Confirm", command=handle_insert)
        confirm_button.pack()
    def remove_data():
        pass
  
    
    add_button = Button(frame2, text="Insert data", command=insert_data)
    add_button.pack()

    remove_button = Button(frame2, text="Remove data", command=remove_data)
    remove_button.pack()

    # Add widgets to frame2
    label3 = Label(frame3, text="2 Engineers and a hunger for perfected password manager.")
    label3.pack()
    notebook.add(frame1, text="Passwords")
    notebook.add(frame2, text="Add/remove passwords")
    notebook.add(frame3, text="About us")

    # Render the menus
    notebook.pack(fill=BOTH, expand=True)

    root.mainloop()

