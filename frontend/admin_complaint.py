import tkinter as tk
from tkinter import ttk, Button, Toplevel, Label, Entry, Text, StringVar, messagebox

class AdminComplaint(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to center the treeview
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        # Create a treeview for displaying complaints
        columns = ('CMS', 'Date', 'Complaint Detail', 'Status', 'Response')
        self.complaint_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        # Set column headings
        for col in columns:
            self.complaint_tree.heading(col, text=col)

        # Set column widths
        self.complaint_tree.column('CMS', width=80)
        self.complaint_tree.column('Date', width=120)
        self.complaint_tree.column('Complaint Detail', width=300)
        self.complaint_tree.column('Status', width=80)
        self.complaint_tree.column('Response', width=300)

        self.complaint_tree.pack(padx=20, pady=40, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.complaint_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.complaint_tree.configure(yscrollcommand=scrollbar.set)

        # Bind double click on treeview item to show complaint details
        self.complaint_tree.bind("<Double-1>", self.show_complaint_details)

        # Placeholder data for complaints (CMS, Date, Complaint Detail, Status, Response)
        complaints_data = [
            ('123456', '2023-01-01', 'Water leakage in room', 'Pending', ''),
            ('654321', '2023-02-15', 'Internet not working', 'Approved', 'Issue resolved.'),
            ('987654', '2023-03-20', 'Broken furniture', 'Rejected', 'Not our responsibility.')
        ]

        # Insert placeholder data into the treeview
        for complaint in complaints_data:
            self.complaint_tree.insert('', 'end', values=complaint)

    def show_complaint_details(self, event):
        # Get the selected item from the treeview
        selected_item = self.complaint_tree.selection()

        if not selected_item:
            return

        # Extract complaint details from the selected item
        item_values = self.complaint_tree.item(selected_item)['values']
        cms, date, complaint_detail, status, response = item_values

        # Create a pop-up window to edit complaint details
        edit_window = Toplevel(self.master)
        edit_window.title('Edit Complaint Details')

        # Create labels and entry fields for editing
        tk.Label(edit_window, text='CMS:').grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(edit_window, state='readonly', textvariable=StringVar(value=cms)).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='Date:').grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(edit_window, state='readonly', textvariable=StringVar(value=date)).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='Complaint Detail:').grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(edit_window, state='readonly', textvariable=StringVar(value=complaint_detail)).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='Status:').grid(row=3, column=0, padx=10, pady=5)
        status_var = StringVar(value=status)
        status_entry = ttk.Combobox(edit_window, textvariable=status_var, values=['Pending', 'Approved', 'Rejected'])
        status_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='Response:').grid(row=4, column=0, padx=10, pady=5)
        response_entry = Text(edit_window, height=4, width=30)
        response_entry.insert('1.0', response)
        response_entry.grid(row=4, column=1, padx=10, pady=5)

        # Save button to update complaint details
        save_button = Button(edit_window, text='Save', command=lambda: self.save_complaint_details(edit_window, selected_item, status_var.get(), response_entry.get("1.0", "end-1c")))
        save_button.grid(row=5, column=1, pady=10)

    def save_complaint_details(self, edit_window, selected_item, new_status, new_response):
    # Get the actual item values from the treeview
        item_values = self.complaint_tree.item(selected_item)['values']

    # Update the treeview with new status and response
        self.complaint_tree.item(selected_item, values=(item_values[0], item_values[1], item_values[2], new_status, new_response))

    # Close the pop-up window
        edit_window.destroy()


if __name__ == "__main__":
    # Add this block to the end of your existing code
    app = MainWindow()
    app.create_admin_dashboard()  # Add this line to create the admin dashboard
    app.admin_complaint = AdminComplaint(app.admin_dashboard)  # Create the AdminComplaint instance
    app.mainloop()
