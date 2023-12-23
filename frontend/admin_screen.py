import tkinter as tk

class AdminScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="Welcome to the Admin Dashboard", font=('Arial', 20))
        label.pack(pady=20)