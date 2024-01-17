import os, sys, stat
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory

#start initializing database, going to use SQLite
def init_db(db_path):
    print(db_path)
