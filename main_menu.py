import sys
import sqlite3
import hashlib
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Style
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
import auth_2fa
import qrcode
from io import BytesIO
import tkinter as tk
from PIL import ImageTk, Image
import pyotp
import json
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
     else:
          messagebox.showwarning("Invalid input.", "Passwords didn't match.")



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
    config_file_path = 'conf.json'
    with open(config_file_path, 'r') as file:
         config = json.load(file)
    global tree
    # Shut down program once you close the window
    def on_closing():
        root.destroy()
        sys.exit()
    
    
    def logout():
     root.destroy()
     main.login_menu(db_path)

    def enable_2fa():
        encrypted_secret, secret = auth_2fa.initialize_2fa(user, salt)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT secret FROM user_auth WHERE user = ?", (user,))
        row = c.fetchone()
        if row is not None and row[0] is not None:
             messagebox.showerror("Error", "2FA already installed.")
        else:
             uri = pyotp.totp.TOTP(secret).provisioning_uri(name=f"{user}", issuer_name="PwManager")
             qr = qrcode.make(uri)
             # Convert the image to an in-memory byte stream
             img_byte_stream = BytesIO()
             qr.save(img_byte_stream, format='PNG')
             img_byte_stream.seek(0)
             # Open the QR code image
             qr_image = Image.open(img_byte_stream)
             qr_image.show()
             totp = pyotp.TOTP(secret)
             qr_verify = simpledialog.askstring("QR installer", "Enter 2fa code to confirm: ")
             if qr_verify is None:
                return 
             if qr_verify == totp.now():
                  c.execute("UPDATE user_auth SET secret = ? WHERE user = ?", (encrypted_secret, user))
                  messagebox.showinfo("Success", "You have successfully activated 2fa.")
             else:
                  messagebox.showerror("Error", "Wrong code for 2fa activation.")
                  re_enter_2fa(totp, encrypted_secret)
             conn.commit()
             conn.close()
             
    def re_enter_2fa(totp, encrypted_secret):
        qr_verify = simpledialog.askstring("QR installer", "Enter 2fa code to confirm: ")
        if qr_verify is None:
             return 
        if qr_verify == totp.now():
                  c.execute("UPDATE user_auth SET secret = ? WHERE user = ?", (encrypted_secret, user))
                  messagebox.showinfo("Success", "You have successfully activated 2fa.")
        else:
             messagebox.showerror("Error", "Wrong code for 2fa activation.")
             re_enter_2fa(totp, encrypted_secret)
         
        
    #Get background and text colors from conf.json and save them into textcolor and bgcolor       
    def bg_color():
         return config["settings"]["bgmode"]
    def text_color():
         return config["settings"]["textmode"]
    def switch_mode():
        config_file_path = 'conf.json'
        with open(config_file_path, 'r') as file:
            config = json.load(file)
        placeholder = config["settings"]["textmode"]
        config["settings"]["textmode"] = config["settings"]["bgmode"]
        config["settings"]["bgmode"] = placeholder
        with open(config_file_path, 'w') as file:
            json.dump(config, file, indent=4)
        root.destroy()
        mainmenu(user, db_path)
        

         
    
    textcolor = text_color()
    bgcolor = bg_color()

    root = Tk()
    root.configure(background=bgcolor)
    root.geometry("800x600")
    frame = Frame(root, bg=bgcolor)
    frame.pack()
    

    

    # Welcome text
    root.resizable(False, False)
    label = Label(frame, text=f"Hello {user}!", background=bgcolor, fg=textcolor)
    label.pack()

    # Call function on_closing after exiting window
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Title of the window
    root.title(f"Password Manager {main.get_version()}")
    

    # Add 3 windows for switching menus
    s = ttk.Style()
    s.configure('My.TFrame', foreground=textcolor, background=bgcolor)
    s.map('My.TFrame', background=[('selected', 'blue')], foreground=[('selected', 'white')])
    s.configure('TNotebook.Tab', background=bgcolor, foreground=textcolor)
    s.map('TNotebook.Tab', background=[('selected', bgcolor)], foreground=[('selected', textcolor)])
    notebook = ttk.Notebook(root, style='My.TFrame')
    frame1 = ttk.Frame(notebook, style='My.TFrame')
    frame2 = ttk.Frame(notebook, style='My.TFrame')
    frame3 = ttk.Frame(notebook, style='My.TFrame')
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
    login_frame = tk.Frame(frame1, background=bgcolor)
    login_frame.grid(row=0, column=0, padx=10, pady=10)

    user_label = Label(login_frame, text="New User:", fg=textcolor, bg=bgcolor)
    user_label.grid(row=0, column=0, sticky="w")
    username_entry = Entry(login_frame, fg=textcolor, bg=bgcolor, insertbackground=textcolor)
    username_entry.grid(row=0, column=1)

    password_label = Label(login_frame, text="Password:", fg=textcolor, bg=bgcolor)
    password_label.grid(row=1, column=0, sticky="w")
    password_entry = Entry(login_frame, show="*", fg=textcolor, bg=bgcolor, insertbackground=textcolor)  # Show asterisks for password
    password_entry.grid(row=1, column=1)

    repassword_label = Label(login_frame, text="Confirm Password:",fg=textcolor,bg=bgcolor)
    repassword_label.grid(row=2, column=0, sticky="w")
    repassword_entry = Entry(login_frame, show="*", fg=textcolor, bg=bgcolor, insertbackground=textcolor)  # Show asterisks for password
    repassword_entry.grid(row=2, column=1)

    register_button = tk.Button(frame1, text="Create User", command=lambda: new_user(username_entry, password_entry, repassword_entry), background=bgcolor, fg=textcolor)
    register_button.grid(row=2, column=0)

    mode_button = tk.Button(frame3, text="Toggle dark/light mode", command=switch_mode, bg=bgcolor, fg=textcolor)
    mode_button.pack()

    logout_button = tk.Button(frame1, text="Logout", command=logout, bg=bgcolor, fg=textcolor)
    logout_button.grid(row=2, column=15)

    auth_fa = tk.Button(frame1, text="Enable 2FA", command=enable_2fa, bg=bgcolor, fg=textcolor)
    auth_fa.grid(row=2, column=16)

    

    #Not too sure why first service doesnt work, but add 3 columns which work.
    tree = ttk.Treeview(frame2, columns=("Service", "Username", "Password"), show="headings", height=20, style='My.TFrame')
    tree.heading("#0", text="Service")
    tree.heading("#1", text="Service")
    tree.heading("#2", text="Username")
    tree.heading("#3", text="Password")
    #center text 
    tree.column("#0", anchor="center")
    tree.column("#1", anchor="center")
    tree.column("#2", anchor="center")
    tree.column("#3", anchor="center")

    y_scrollbar = Scrollbar(frame2, orient="vertical", command=tree.yview, background=bgcolor)
    y_scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=y_scrollbar.set, style="My.TFrame")
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
        input_window = Toplevel(frame2, background=bgcolor)
        input_window.title("Insert Data")
        input_window.configure(background=bgcolor)
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
        service_label = Label(input_window, text="Service:", bg=bgcolor, fg=textcolor)
        service_label.pack()
        service_entry = Entry(input_window, fg=textcolor, bg=bgcolor, insertbackground=textcolor)
        service_entry.pack()
        
        service_entry.focus_set()

        username_label = Label(input_window, text="Username:", bg=bgcolor, fg=textcolor)
        username_label.pack()
        username_entry = Entry(input_window, fg=textcolor, bg=bgcolor, insertbackground=textcolor)
        username_entry.pack()

        password_label = Label(input_window, text="Password:", bg=bgcolor, fg=textcolor)
        password_label.pack()
        password_entry = Entry(input_window, fg=textcolor, bg=bgcolor, insertbackground=textcolor) 
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

        generate_pwbutton = Button(input_window, text="Generate password", command=generate_password, bg=bgcolor, fg=textcolor)
        generate_pwbutton.pack()



        # Button to confirm and insert data
        confirm_button = Button(input_window, text="Confirm", command=handle_insert, bg=bgcolor, fg=textcolor)
        confirm_button.pack()
        input_window.bind("<Return>", lambda event: handle_insert())

    def remove_data():
        confirm = False #make sure confirm is False by default.
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import padding
        except Exception as e:
            return messagebox.showerror("Error occurred", e)
        
        selected_items = tree.selection()
        if not selected_items:
            return
        confirm = messagebox.askyesno("Are you sure?", "Deleting will PERMANENTLY remove selected data.")
        if confirm == False:
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
            conn.commit()
            conn.close()
            update_interface(db_path, user, crypter)
    add_button = Button(frame2, text="Insert data", command=insert_data, bg=bgcolor, fg=textcolor)
    add_button.pack()

    remove_button = Button(frame2, text="Remove data", command=remove_data, bg=bgcolor, fg=textcolor)
    remove_button.pack()

    # Add widgets to frame2
    label3 = Label(frame3, text="2 Engineers and a hunger for perfected password manager.", bg=bgcolor, fg=textcolor)
    label3.pack()
    label4 = Label(frame3, text=f"Random fact of the day: {random_fact}", bg=bgcolor, fg=textcolor)
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

