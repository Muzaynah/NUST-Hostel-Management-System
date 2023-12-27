import tkinter as tk
from tkinter import Button, Entry, Label, Listbox, Scrollbar, StringVar, OptionMenu, messagebox
from datetime import datetime
import mysql.connector
from config import db_config

class StudentAttendance(tk.Frame):
    def __init__(self, master, show_dashboard):
        super().__init__(master)
        self.master = master
        self.show_dashboard = show_dashboard
        #self.create_widgets()