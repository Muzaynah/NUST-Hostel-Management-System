import tkinter as tk
from tkinter import Entry, Label, Button
from PIL import Image, ImageTk
from backend.authentication import authenticate_user
import mysql.connector


#1f2b38 dark
#E0E6EE bg light
#014a81 nust blue
#2270ab lighter nust blue

class LoginPage(tk.Frame):
    def __init__(self, master, show_admin_page, show_student_page):
        super().__init__(master)
        self.master = master
        self.show_admin_page = show_admin_page
        self.show_student_page = show_student_page
        self.create_widgets()

    def create_widgets(self):
        # Login frame
        login_frame = tk.Frame(self, width=360, height=360, bg='#1a2530')  # Use the same dark blue color
        login_frame.pack(side="top", pady=160)

        Label(login_frame, text='Sign In', fg='#3a80b5', bg='#1a2530',  # Use the same light blue color
              font=('Microsoft YaHei UI Light', 26, 'bold')).pack(padx=20, pady=(40, 50))

        # Username
        def on_enter_username(e):
            name = self.user.get()
            if name == 'Username':
                self.user.delete(0, 'end')

        def on_leave_username(e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Username')

        self.user = Entry(login_frame, width=35, fg='white', border=0, bg='#1a2530',  # Use the same dark blue color
                          font=('Microsoft YaHei UI Light', 11))
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', on_enter_username)
        self.user.bind('<FocusOut>', on_leave_username)
        self.user.pack(padx=20, pady=10)

        tk.Frame(login_frame, width=295, height=2, bg='white').pack(padx=20)  # Use white color for the separator

        # Password
        def on_enter_password(e):
            pw = self.password.get()
            if pw == 'Password':
                self.password.delete(0, 'end')

        def on_leave_password(e):
            pw = self.password.get()
            if pw == '':
                self.password.insert(0, 'Password')

        self.password = Entry(login_frame, width=35, fg='white', border=0, bg='#1a2530',  # Use the same dark blue color
                              font=('Microsoft YaHei UI Light', 11))
        self.password.insert(0, 'Password')
        self.password.bind('<FocusIn>', on_enter_password)
        self.password.bind('<FocusOut>', on_leave_password)
        self.password.pack(padx=20, pady=10)

        tk.Frame(login_frame, width=295, height=2, bg='white').pack(padx=20)  # Use white color for the separator

        Button(login_frame, width=26, pady=6, text='Sign In', bg='#014a81', fg='white',font=('Microsoft YaHei UI Light', 14),
               border=0, command=self.sign_in).pack(padx=30, pady=(130,30))

    def sign_in(self):
        username = self.user.get()
        pw = self.password.get()

        user = authenticate_user(username, pw)
        if user == 'admin':
            self.show_admin_page()
        elif user == 'student':
            self.show_student_page()
        elif user == 'invalid':
            print('invalid sign in')
            # invalid sign-in label logic here

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root, show_admin_page=lambda: print("Admin Page"),
                    show_student_page=lambda: print("Student Page"))
    app.pack()
    root.mainloop()