#student_screen.py

import tkinter as tk

class StudentScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="Welcome to the Student Dashboard", font=('Arial', 20))
        label.pack(pady=20)
        #self.create_widgets()

    #def create_widgets(self):
        # student screen code 