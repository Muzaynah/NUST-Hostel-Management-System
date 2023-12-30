import tkinter as tk
from tkinter import Entry, Label, Button
from backend.authentication import authenticate_user,authenticate_username
import config

class LoginPage(tk.Frame):
    def __init__(self, master, show_admin_dashboard, show_student_dashboard, show_password_reset):
        super().__init__(master)
        self.master = master
        self.show_admin_dashboard = show_admin_dashboard
        self.show_student_dashboard = show_student_dashboard
        self.show_password_reset = show_password_reset
        self.message_text = tk.StringVar()
        self.create_widgets()

    def update_message_label(self,message):
        new_text=message
        self.message_text.set(new_text)

    def create_widgets(self):

        login_frame = tk.Frame(self, width=360, height=360, bg='#1a2530')
        login_frame.pack(side="top",pady=(160,0))


        Label(login_frame, text='Sign In', fg='#3a80b5', bg='#1a2530',
              font=('Microsoft YaHei UI Light', 26, 'bold')).pack(padx=20, pady=(40, 50))

        message_frame = tk.Frame(self, width=360, height=50, bg='#F0F0F0')  # Adjusted height
        message_frame.pack(side="top",pady=(10,0))

        message_label =Label(message_frame, textvariable=self.message_text, fg='#FF0000',
              font=('Microsoft YaHei UI Light', 16))
        message_label.pack()

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

        # Button(login_frame, width=26, pady=6, text='Sign In', bg='#014a81', fg='white',font=('Microsoft YaHei UI Light', 14), border=0, command=self.sign_in).pack(padx=30, pady=(130,30))
        Button(login_frame, width=26, pady=6, text='Sign In', bg='#014a81', fg='white',font=('Microsoft YaHei UI Light', 14), border=0, command=self.sign_in).pack(padx=30, pady=(10,5))

        # Button(login_frame, width=26, pady=6, text='Forgot Password', bg='#014a81', fg='white',font=('Microsoft YaHei UI Light', 14), border=0, command=self.show_password_reset).pack(padx=30, pady=(10,30))
        Button(login_frame, width=26, pady=6, text='Forgot Password', bg='#014a81', fg='white',font=('Microsoft YaHei UI Light', 14), border=0, command=self.forgot_password_clicked).pack(padx=30, pady=(10,10))
        

    def sign_in(self):
        # global current_user_id
        username = self.user.get()
        pw = self.password.get()

        user_type, user_id = authenticate_user(username, pw)
        if user_type == 'manager':
            id = user_id
            config.current_user_id = id
            print('manager logging in')
            self.show_admin_dashboard()
        elif user_type == 'student':
            id = user_id
            config.current_user_id = id
            print('student logging in')
            self.show_student_dashboard()
        elif user_type == 'invalid':
            self.update_message_label("Invalid Login")

    def forgot_password_clicked(self):
        username=self.user.get()
        if(username==""):
            self.update_message_label("Enter username")
            return
        result=authenticate_username(username)
        if(result[0]=='invalid'):
            self.update_message_label("Invalid username")
            return
        elif(result[0]=='student'):
            config.current_user_id = result[1]
            config.current_user_type="Student"
            self.show_password_reset()
        elif(result[0]=='manager'):
            config.current_user_id=result[1]
            config.current_user_type="Manager"
            self.show_password_reset()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root, show_admin_dashboard=lambda: print("Admin Page"),
                    show_student_dashboard=lambda: print("Student Page"))
    app.pack()
    root.mainloop()