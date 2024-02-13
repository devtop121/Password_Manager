import sys
import sqlite3
import hashlib
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import simpledialog
import dbmodify
import requests
from cryptography.fernet import Fernet
import validator
import main
import secrets
import string
import os
from dotenv import load_dotenv
import base64
global tree

def new_user(user_entry, password_entry, repassword_entry):
     password = password_entry.get()
     repassword = repassword_entry.get()
     user = user_entry.get()
     pathdb = "C:/pwpath/path.txt"
     with open(pathdb, 'r') as file:
        db_path = file.read()
     if password == repassword:
          validator.validate_password(user, password, db_path)

    
#Get a random fact of the day
def daily_random():
    api_url = 'https://uselessfacts.jsph.pl/'
    endpoint = '/api/v2/facts/today'
    full_url = f'{api_url}{endpoint}'
    response = requests.get(full_url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content (assuming it's in JSON format)
        return response.json().get('text')
    else:
        return "Couldn't load daily fact."
    
#call the function and store answer in random_fact
random_fact = daily_random()

#rows contains the database for said user
def populate_treeview(tree, rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=row)

def mainmenu(user, db_path):
    global tree
    # Shut down program once you close the window
    def on_closing():
        root.destroy()
        sys.exit()
    
    def logout():
     root.destroy()
     main.login_menu(db_path)
        
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
    root.title(f"Password Manager {main.get_version()}")

    # Add 2 windows for switching menus
    notebook = ttk.Notebook(root)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    frame3 = ttk.Frame(notebook)
    #connect to the database to get users information

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT website, username, password FROM passwords WHERE user = ?", (user,))
    rows = c.fetchall()
    c.execute("SELECT salt FROM user_auth WHERE user = ?", (user,))
    salt = c.fetchone()
    salt = salt[0]
    salt = salt.encode('utf-8')
    load_dotenv()
    key = os.getenv('key')
    key = key[2:-1]
    key = key.encode('utf-8')
    combined_key = key + salt
    crypter = Fernet(combined_key)
    def decrypt_value(encrypted_value):
            return crypter.decrypt(encrypted_value).decode('utf-8')
    decrypted_list = [(item[0], item[1], decrypt_value(item[2])) for item in rows]
    c.execute("SELECT salt FROM user_auth WHERE user = ?", (user,))
    salt = c.fetchone()
    conn.close()

    # Add widgets to frame1
    login_frame = ttk.Frame(frame1)
    login_frame.grid(row=0, column=0, padx=10, pady=10)

    user_label = Label(login_frame, text="New User:")
    user_label.grid(row=0, column=0, sticky="w")
    username_entry = Entry(login_frame)
    username_entry.grid(row=0, column=1)

    password_label = Label(login_frame, text="Password:")
    password_label.grid(row=1, column=0, sticky="w")
    password_entry = Entry(login_frame, show="*")  # Show asterisks for password
    password_entry.grid(row=1, column=1)

    repassword_label = Label(login_frame, text="Confirm Password:")
    repassword_label.grid(row=2, column=0, sticky="w")
    repassword_entry = Entry(login_frame, show="*")  # Show asterisks for password
    repassword_entry.grid(row=2, column=1)

    register_button = ttk.Button(frame1, text="New user", command=lambda: new_user(username_entry, password_entry, repassword_entry))
    register_button.grid(row=2, column=0)

    logout_button = ttk.Button(frame1, text="Logout", command=logout)
    logout_button.grid(row=2, column=15)

    #Not too sure why first service doesnt work, but add 3 columns which work.
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
    populate_treeview(tree, decrypted_list)

    tree.pack()
    #if a window is open to prevent multiple opening when spamming
    input_window_open = False

    def insert_data():
        if getattr(insert_data, 'input_window_open', False):
            return
        insert_data.input_window_open = True

        def on_close():
            insert_data.input_window_open = False
            input_window.destroy()
    # Function to handle the insertion of data
        def handle_insert():
            # Get values from entry widgets
            service = service_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            # Close the input window
            input_window.destroy()
            insert_data.input_window_open = False
            dbmodify.add_data(db_path, user, service, username, password)

            
    
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
        input_window.protocol("WM_DELETE_WINDOW", on_close)

        # Entry widgets for user input
        service_label = Label(input_window, text="Service:")
        service_label.pack()
        service_entry = Entry(input_window)
        service_entry.pack()
        
        service_entry.focus_set()

        username_label = Label(input_window, text="Username:")
        username_label.pack()
        username_entry = Entry(input_window)
        username_entry.pack()

        password_label = Label(input_window, text="Password:")
        password_label.pack()
        password_entry = Entry(input_window) 
        password_entry.pack()

        def generate_password():
             characters = string.ascii_letters + string.digits + string.punctuation
             length = secrets.choice(range(12,17))
             password = ''.join(secrets.choice(characters) for i in range(length))
             while (not any(c.isupper() for c in password) or
                    not any(c.islower() for c in password) or
                    not any(c.isdigit() for c in password) or
                    not any(c in string.punctuation for c in password)):
                password = ''.join(secrets.choice(characters) for i in range(length))
             password_entry.delete(0, END)
             password_entry.insert(0, password)

        generate_pwbutton = Button(input_window, text="Generate password", command=generate_password)
        generate_pwbutton.pack()



        # Button to confirm and insert data
        confirm_button = Button(input_window, text="Confirm", command=handle_insert)
        confirm_button.pack()
        input_window.bind("<Return>", lambda event: handle_insert())

    def remove_data():
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import padding
        except Exception as e:
            print(e)
            return
        
        selected_items = tree.selection()

        if not selected_items:
            print("No items selected")
            return
        
        for item in selected_items:
            values = tree.item(item, 'values')
            website, username, password = values  # Assuming this order of values
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT salt FROM user_auth WHERE user = ?", (user,))
            salt = c.fetchone()
            salt = salt[0]
            password = password + salt
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # Find the corresponding id for the given website, username, and password
            c.execute("SELECT id FROM passwords WHERE user = ? AND website = ? AND username = ? AND hashed_password = ?", (user, website, username, password))
            result = c.fetchone()
            if result:
                primary_key = result[0]
                # Perform the removal logic in the database
                c.execute("DELETE FROM passwords WHERE id = ?", (primary_key,))
                print(f"Removed data successfully")
            else:
                print("No corresponding record found for deletion.")
            conn.commit()
            conn.close()
            update_interface(db_path, user, crypter)
            
    add_button = Button(frame2, text="Insert data", command=insert_data)
    add_button.pack()

    remove_button = Button(frame2, text="Remove data", command=remove_data)
    remove_button.pack()

    # Add widgets to frame2
    label3 = Label(frame3, text="2 Engineers and a hunger for perfected password manager.")
    label3.pack()
    label4 = Label(frame3, text=f"Random fact of the day: {random_fact}")
    label4.pack()

    notebook.add(frame1, text="Manage users")
    notebook.add(frame2, text="Passwords")
    notebook.add(frame3, text="About us")

    # Render the menus
    notebook.pack(fill=BOTH, expand=True)

    root.mainloop()

def decrypt_value(encrypted_value, crypter):
            return crypter.decrypt(encrypted_value).decode('utf-8')

def update_interface(db_path, user, crypter):
        global tree
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT website, username, password FROM passwords WHERE user = ?", (user,))
        rows = c.fetchall()
        decrypted_list = [(item[0], item[1], decrypt_value(item[2], crypter)) for item in rows]
        c.execute("SELECT salt FROM user_auth WHERE user = ?", (user,))
        salt = c.fetchone()
        conn.close()
        populate_treeview(tree, decrypted_list)
        return decrypted_list

