import tkinter as tk
from tkinter import Button, Label, Text, OptionMenu, StringVar, messagebox, ttk
from datetime import datetime
import mysql.connector
from config import db_config

class StudentComplaint(tk.Frame):
    def __init__(self, master, show_dashboard):
        super().__init__(master)
        self.master = master
        self.show_dashboard = show_dashboard
        self.complaint_data = []  # Store complaint data temporarily
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the left section (file complaints)
        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the right section (complaint history)
        right_frame = tk.Frame(self, width=800, height=600, bg='white')  # Increased width for the right frame
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File Complaint section (Left Frame)
        # Entry widgets for the complaint form
        square_size = 10  # Adjust this value to control the number of visible lines

        # Add some space before the text field
        complaint_text = Text(left_frame, width=30, height=square_size)
        complaint_text.pack(pady=(15, 0))  # Add space only above the text field

        # Date dropdown similar to outpass
        date_label = Label(left_frame, text='Date:')
        date_label.pack()

        day_var = StringVar()
        month_var = StringVar()
        year_var = StringVar()

        day_menu = OptionMenu(left_frame, day_var, *range(1, 32))
        month_menu = OptionMenu(left_frame, month_var, *range(1, 13))
        year_menu = OptionMenu(left_frame, year_var, *range(datetime.now().year, datetime.now().year + 1))

        day_menu.pack()
        month_menu.pack()
        year_menu.pack()

        # Add some space between the date dropdown and the submit button
        submit_button = Button(left_frame, text='File a Complaint', command=lambda: self.submit_complaint(
            complaint_text.get("1.0", "end-1c"),
            day_var.get(), month_var.get(), year_var.get()
        ))
        submit_button.pack(pady=(15, 0), ipadx=10, ipady=5)  # Add space only above the submit button

        # Complaint History section (Right Frame)
        Label(right_frame, text='Complaint History', font=('Helvetica', 16)).pack(pady=20)

        # Treeview to display complaint history
        columns = ('Complaint', 'Date', 'Description', 'Status')  # Added 'Description' column
        self.complaint_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.complaint_tree.heading(col, text=col)
        self.complaint_tree.pack(pady=10)

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.complaint_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.complaint_tree.config(yscrollcommand=scrollbar.set)

        # Dropdown button for filtering
        filter_options = ["All", "In Progress", "Resolved", "Pending"]
        filter_var = StringVar()
        filter_var.set(filter_options[0])  # Set default value

        filter_menu = OptionMenu(right_frame, filter_var, *filter_options, command=lambda _: self.filter_complaints(self.complaint_tree, filter_var.get()))
        filter_menu.pack(pady=10)

        # Reset button to clear the filter
        reset_button = Button(right_frame, text='Reset', command=lambda: self.filter_complaints(self.complaint_tree, "All"))
        reset_button.pack(pady=5)

        # Back to dashboard button
        Button(self, text='Back to Dashboard', command=self.show_dashboard).pack(pady=20)

    def submit_complaint(self, description, leaving_day, leaving_month, leaving_year):
        # Check if any field is empty
        if not description.strip():  # Use strip to check if it's only whitespace
            messagebox.showerror("Error", "Complaint field must be filled.")
            return

        # Format LeavingDate as a datetime object
        leaving_date = datetime(int(leaving_year), int(leaving_month), int(leaving_day))

        # Add the complaint data to the temporary list
        complaint_data = ("Complaint {}".format(len(self.complaint_data) + 1), leaving_date.strftime("%Y-%m-%d"), description, "Pending")
        self.complaint_data.append(complaint_data)

        # Update the Treeview with the new data
        self.update_complaint_tree()

        # Show success message in a new window centered on the screen
        success_window = tk.Toplevel(self.master)
        success_window.title("Success")

        success_label = Label(success_window, text="Complaint submitted successfully!")
        success_label.pack(padx=20, pady=20)

        ok_button = Button(success_window, text="OK", command=success_window.destroy)
        ok_button.pack(pady=10)

        # Center the success window on the screen
        window_width = success_window.winfo_reqwidth()
        window_height = success_window.winfo_reqheight()

        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        success_window.geometry("+{}+{}".format(x_position, y_position))

    def update_complaint_tree(self):
        # Clear the Treeview
        for child in self.complaint_tree.get_children():
            self.complaint_tree.delete(child)

        # Insert the updated data into the Treeview
        for item in self.complaint_data:
            self.complaint_tree.insert('', tk.END, values=item)

    def filter_complaints(self, treeview, status):
        treeview.delete(*treeview.get_children())  # Clear the treeview

        if status == "All":
            # Insert all complaints
            for item in self.complaint_data:
                treeview.insert('', tk.END, values=item)
        else:
            # Insert filtered complaints
            for item in self.complaint_data:
                if item[3] == status:
                    treeview.insert('', tk.END, values=item)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentComplaint(root, show_dashboard=lambda: print("Back to Dashboard"))
    app.pack()
    root.mainloop()