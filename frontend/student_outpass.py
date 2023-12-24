# student_outpass.py
import tkinter as tk
from tkinter import Button, Entry, Label, Listbox, Scrollbar, StringVar, OptionMenu, messagebox
from datetime import datetime

class StudentOutpass(tk.Frame):
    def __init__(self, master, show_dashboard):
        super().__init__(master)
        self.master = master
        self.show_dashboard = show_dashboard
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the left section (apply for outpass)
        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the right section (outpass log)
        right_frame = tk.Frame(self, width=600, height=600, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Request an outpass section (Left Frame)
        Label(left_frame, text='Request an Outpass', font=('Helvetica', 16)).pack(pady=20)

        # Entry widgets for outpass request form
        purpose_label = Label(left_frame, text='Purpose:')
        purpose_label.pack()
        purpose_entry = Entry(left_frame)
        purpose_entry.pack()

        # Leaving Date
        leaving_date_label = Label(left_frame, text='Leaving Date:')
        leaving_date_label.pack()

        # Drop-down menus for day, month, and year
        day_var = StringVar()
        month_var = StringVar()
        year_var = StringVar()

        day_menu = OptionMenu(left_frame, day_var, *range(1, 32))
        month_menu = OptionMenu(left_frame, month_var, *range(1, 13))
        year_menu = OptionMenu(left_frame, year_var, *range(datetime.now().year, datetime.now().year + 1))

        day_menu.pack()
        month_menu.pack()
        year_menu.pack()

        # Joining Date
        joining_date_label = Label(left_frame, text='Joining Date:')
        joining_date_label.pack()

        # Drop-down menus for day, month, and year
        day_var_joining = StringVar()
        month_var_joining = StringVar()
        year_var_joining = StringVar()

        day_menu_joining = OptionMenu(left_frame, day_var_joining, *range(1, 32))
        month_menu_joining = OptionMenu(left_frame, month_var_joining, *range(1, 13))
        year_menu_joining = OptionMenu(left_frame, year_var_joining, *range(datetime.now().year, datetime.now().year + 1))

        day_menu_joining.pack()
        month_menu_joining.pack()
        year_menu_joining.pack()

        # Submit button
        submit_button = Button(left_frame, text='Submit', command=lambda: self.submit_outpass(
            purpose_entry.get(),
            day_var.get(), month_var.get(), year_var.get(),
            day_var_joining.get(), month_var_joining.get(), year_var_joining.get()
        ))
        submit_button.pack(pady=10)

        # Outpass Log section (Right Frame)
        Label(right_frame, text='Outpass Requests and History', font=('Helvetica', 16)).pack(pady=20)

        # Listbox to display outpass requests and history
        outpass_listbox = Listbox(right_frame, selectmode=tk.SINGLE, width=40, height=15)
        outpass_listbox.pack(pady=10)

        # Example data for the listbox (replace with actual data)
        outpass_data = ["Request 1 - Pending", "Request 2 - Approved", "Request 3 - Rejected"]
        for item in outpass_data:
            outpass_listbox.insert(tk.END, item)

        # Scrollbar for the listbox
        scrollbar = Scrollbar(right_frame, orient=tk.VERTICAL)
        scrollbar.config(command=outpass_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        outpass_listbox.config(yscrollcommand=scrollbar.set)

        # Back to dashboard button
        Button(self, text='Back to Dashboard', command=self.show_dashboard).pack(pady=20)

    def submit_outpass(self, purpose, leaving_day, leaving_month, leaving_year, joining_day, joining_month, joining_year):
        # Check if any field is empty
        if not purpose or not leaving_day or not leaving_month or not leaving_year or not joining_day or not joining_month or not joining_year:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        # Placeholder function for submitting outpass request
        leaving_date = f"{leaving_day}-{leaving_month}-{leaving_year}"
        joining_date = f"{joining_day}-{joining_month}-{joining_year}"

        print(f"Outpass submitted: Purpose={purpose}, Leaving Date={leaving_date}, Joining Date={joining_date}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentOutpass(root, show_dashboard=lambda: print("Back to Dashboard"))
    app.pack()
    root.mainloop()