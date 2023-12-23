import tkinter as tk
from tkinter import Entry, Label, Button
from PIL import Image, ImageTk
from backend.authentication import authenticate_user

class LoginPage(tk.Frame):
    def __init__(self, master, show_admin_page, show_student_page):
        super().__init__(master)
        self.master = master
        self.show_admin_page = show_admin_page
        self.show_student_page = show_student_page
        self.create_widgets()

    def create_widgets(self):

        # Login frame
        login_frame = tk.Frame(self, width=360, height=360, bg='white')
        login_frame.pack(side="top", fill="both", expand=True)

        # Center the frame
        self.master.update_idletasks()  # Update the window to get the correct size
        x_coord = (self.master.winfo_width() - login_frame.winfo_reqwidth()) // 2
        y_coord = (self.master.winfo_height() - login_frame.winfo_reqheight()) // 2
        login_frame.place(x=x_coord, y=y_coord)

        Label(login_frame, text='Sign In', fg='#408eed', bg='white',
              font=('Microsoft YaHei UI Light', 23, 'bold')).pack(pady=10)

        # Username
        def on_enter_username(e):
            name = self.user.get()
            if name == 'Username':
                self.user.delete(0, 'end')

        def on_leave_username(e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Username')

        self.user = Entry(login_frame, width=35, fg='black', border=0, bg='white',
                          font=('Microsoft YaHei UI Light', 11))
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', on_enter_username)
        self.user.bind('<FocusOut>', on_leave_username)
        self.user.pack(pady=10)

        tk.Frame(login_frame, width=295, height=2, bg='black').pack()

        # Password
        def on_enter_password(e):
            pw = self.password.get()
            if pw == 'Password':
                self.password.delete(0, 'end')

        def on_leave_password(e):
            pw = self.password.get()
            if pw == '':
                self.password.insert(0, 'Password')

        self.password = Entry(login_frame, width=35, fg='black', border=0, bg='white',
                              font=('Microsoft YaHei UI Light', 11))
        self.password.insert(0, 'Password')
        self.password.bind('<FocusIn>', on_enter_password)
        self.password.bind('<FocusOut>', on_leave_password)
        self.password.pack(pady=10)

        tk.Frame(login_frame, width=295, height=2, bg='black').pack()

        Button(login_frame, width=39, pady=7, text='Sign In', bg='#408eed', fg='white',
               border=0, command=self.sign_in).pack(pady=20)

    def sign_in(self):
        username = self.user.get()
        pw = self.password.get()

        # Assuming authenticate_user returns True for successful authentication
        if authenticate_user(username, pw):
            if username == 'admin':
                self.show_admin_page()
            elif username == 'student':
                self.show_student_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root, show_admin_page=lambda: print("Admin Page"),
                    show_student_page=lambda: print("Student Page"))
    app.pack()
    root.mainloop()