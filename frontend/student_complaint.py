import tkinter as tk
from tkinter import Button, Label, Text, OptionMenu, StringVar, messagebox, ttk
from datetime import datetime
import mysql.connector
from config import db_config_student
import config

class StudentComplaint(tk.Frame):
    def __init__(self, master, show_dashboard):
        super().__init__(master)
        self.master = master
        self.show_dashboard = show_dashboard
        self.complaint_data = []
        self.create_widgets()
        self.connect_to_database()

    def create_widgets(self):
        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self, width=800, height=600, bg='white') 
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        square_size = 10
        self.complaint_text = Text(left_frame, width=30, height=square_size)
        self.complaint_text.pack(pady=(15, 0))

        date_label = Label(left_frame, text='Date:')
        date_label.pack()

        self.leaving_day_var = StringVar()
        self.leaving_month_var = StringVar()
        self.leaving_year_var = StringVar()

        day_menu = OptionMenu(left_frame, self.leaving_day_var, *range(1, 32))
        month_menu = OptionMenu(left_frame, self.leaving_month_var, *range(1, 13))
        year_menu = OptionMenu(left_frame, self.leaving_year_var, *range(datetime.now().year, datetime.now().year + 1))

        day_menu.pack()
        month_menu.pack()
        year_menu.pack()

        submit_button = Button(left_frame, text='File a Complaint', command=self.submit_complaint)
        submit_button.pack(pady=(15, 0), ipadx=10, ipady=5)

        reset_button = Button(left_frame, text='Reset', command=self.reset_fields)
        reset_button.pack(pady=5)

        Label(right_frame, text='Complaint History', font=('Helvetica', 16)).pack(pady=20)

        columns = ('Complaint', 'Date', 'Description', 'Status')
        self.complaint_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.complaint_tree.heading(col, text=col)
        self.complaint_tree.pack(pady=10)

        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.complaint_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.complaint_tree.config(yscrollcommand=scrollbar.set)

        filter_options = ["All", "In Progress", "Resolved", "Pending"]
        self.filter_var = StringVar()
        self.filter_var.set(filter_options[0])

        filter_menu = OptionMenu(right_frame, self.filter_var, *filter_options, command=lambda _: self.filter_complaints(self.complaint_tree, self.filter_var.get()))
        filter_menu.pack(pady=10)

        reset_button = Button(right_frame, text='Reset', command=lambda: self.filter_complaints(self.complaint_tree, "All"))
        reset_button.pack(pady=5)

        Button(self, text='Back to Dashboard', command=self.show_dashboard).pack(pady=20)

    def connect_to_database(self):
        self.conn = mysql.connector.connect(**db_config_student)
        self.cursor = self.conn.cursor()

    def submit_complaint(self):
        description = self.complaint_text.get("1.0", "end-1c")
        if not description.strip():
            messagebox.showerror("Error", "Complaint field must be filled.")
            return

        leaving_date = datetime(int(self.leaving_year_var.get()), int(self.leaving_month_var.get()), int(self.leaving_day_var.get()))

        complaint_data = ("Complaint {}".format(len(self.complaint_data) + 1), leaving_date.strftime("%Y-%m-%d"), description, "Pending")
        self.complaint_data.append(complaint_data)

        self.update_complaint_tree()
        self.insert_complaint_into_db(description, leaving_date, "Pending")

        success_window = tk.Toplevel(self.master)
        success_window.title("Success")

        success_label = Label(success_window, text="Complaint submitted successfully!")
        success_label.pack(padx=20, pady=20)

        ok_button = Button(success_window, text="OK", command=success_window.destroy)
        ok_button.pack(pady=10)

        window_width = success_window.winfo_reqwidth()
        window_height = success_window.winfo_reqheight()

        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        success_window.geometry("+{}+{}".format(x_position, y_position))

        # Reset fields after submission
        self.reset_fields()

    def insert_complaint_into_db(self, description, leaving_date, status):
        insert_query = """
        INSERT INTO Complaint (CDescription, CStatus, CDate, cms)
        VALUES (%s, %s, %s, %s);
        """
        cms_id = config.current_user_id[0]
        data = (description, status, leaving_date.strftime('%Y-%m-%d'), cms_id)

        try:
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            print("Complaint inserted into the database successfully!")

        except Exception as e:
            print(f"Error: {e}")

    def update_complaint_tree(self):
        for child in self.complaint_tree.get_children():
            self.complaint_tree.delete(child)

        for item in self.complaint_data:
            self.complaint_tree.insert('', tk.END, values=item)

    def filter_complaints(self, treeview, status):
        treeview.delete(*treeview.get_children())

        if status == "All":
            for item in self.complaint_data:
                treeview.insert('', tk.END, values=item)
        else:
            for item in self.complaint_data:
                if item[3] == status:
                    treeview.insert('', tk.END, values=item)

    def reset_fields(self):
        self.complaint_text.delete('1.0', tk.END)
        self.leaving_day_var.set('')
        self.leaving_month_var.set('')
        self.leaving_year_var.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentComplaint(root, show_dashboard=lambda: print("Back to Dashboard"))
    app.pack()
    root.mainloop()
