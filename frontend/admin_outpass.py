import tkinter as tk
from tkinter import Button, ttk, Label, Toplevel, StringVar

class AdminOutpass(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to center the treeview
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        # Create a treeview for displaying outpasses
        columns = ('Purpose', 'Leaving Date', 'Leaving Month', 'Leaving Year', 'Joining Date', 'Joining Month', 'Joining Year',
                   'Guardian 1 Contact', 'Guardian 2 Contact', 'Guardian 3 Contact', 'Status')
        self.outpass_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        # Set column headings
        self.outpass_tree.heading('Purpose', text='Purpose')
        self.outpass_tree.heading('Leaving Date', text='Leaving Date')
        self.outpass_tree.heading('Leaving Month', text='Leaving Month')
        self.outpass_tree.heading('Leaving Year', text='Leaving Year')
        self.outpass_tree.heading('Joining Date', text='Joining Date')
        self.outpass_tree.heading('Joining Month', text='Joining Month')
        self.outpass_tree.heading('Joining Year', text='Joining Year')
        self.outpass_tree.heading('Guardian 1 Contact', text='Guardian 1 Contact')
        self.outpass_tree.heading('Guardian 2 Contact', text='Guardian 2 Contact')
        self.outpass_tree.heading('Guardian 3 Contact', text='Guardian 3 Contact')
        self.outpass_tree.heading('Status', text='Status')

        # Set column widths
        self.outpass_tree.column('Purpose', width=100)
        self.outpass_tree.column('Leaving Date', width=80)
        self.outpass_tree.column('Leaving Month', width=80)
        self.outpass_tree.column('Leaving Year', width=80)
        self.outpass_tree.column('Joining Date', width=80)
        self.outpass_tree.column('Joining Month', width=80)
        self.outpass_tree.column('Joining Year', width=80)
        self.outpass_tree.column('Guardian 1 Contact', width=120)
        self.outpass_tree.column('Guardian 2 Contact', width=120)
        self.outpass_tree.column('Guardian 3 Contact', width=120)
        self.outpass_tree.column('Status', width=80)

        self.outpass_tree.pack(padx=20, pady=40, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.outpass_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.outpass_tree.configure(yscrollcommand=scrollbar.set)

        # Bind double click on treeview item to open edit window
        self.outpass_tree.bind('<Double-1>', self.edit_outpass_details)

        dummy_data = [
            ('Study', '01', '02', '2023', '02', '02', '2023', '1234567890', '9876543210', '6543210987', 'Pending'),
            ('Family Visit', '15', '03', '2023', '18', '03', '2023', '9876543210', '1234567890', '3456789012', 'Approved'),
            ('Medical Emergency', '05', '04', '2023', '10', '04', '2023', '7890123456', '2345678901', '9012345678', 'Rejected'),
            # Add more dummy data as needed
        ]

        # Insert dummy data into the treeview
        for data in dummy_data:
            self.outpass_tree.insert('', 'end', values=data)

    def edit_outpass_details(self, event):
        # Get the selected item
        selected_item = self.outpass_tree.selection()[0]

        # Create a pop-up window for editing outpass details
        edit_window = Toplevel(self)
        edit_window.title('Edit Outpass Details')

        # Get the actual item values from the treeview
        item_values = self.outpass_tree.item(selected_item)['values']

        # Create labels and entry fields for outpass information
        labels = ['Purpose', 'Leaving Date', 'Leaving Month', 'Leaving Year', 'Joining Date', 'Joining Month', 'Joining Year',
                  'Guardian 1 Contact', 'Guardian 2 Contact', 'Guardian 3 Contact']

        entry_fields = {}
        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).grid(row=i, column=0, pady=5, padx=5)
            entry = Label(edit_window, text=str(item_values[i]))
            entry.grid(row=i, column=1, pady=5, padx=5)
            entry_fields[label] = entry

        # Create a dropdown menu for status
        status_var = StringVar(edit_window)
        status_var.set(item_values[-1])  # Set the default value to the existing status
        status_label = tk.Label(edit_window, text='Status')
        status_label.grid(row=len(labels), column=0, pady=5, padx=5)
        status_menu = ttk.Combobox(edit_window, textvariable=status_var, values=['Pending', 'Approved', 'Rejected'])
        status_menu.grid(row=len(labels), column=1, pady=5, padx=5)

        # Add a button to save the changes
        save_button = Button(edit_window, text='Save', command=lambda: self.save_outpass_details(edit_window, selected_item, entry_fields, status_var))
        save_button.grid(row=len(labels) + 1, columnspan=2, pady=10)

    def save_outpass_details(self, edit_window, selected_item, entry_fields, status_var):
        # Get the new values from the entry fields and dropdown menu
        new_values = [entry.cget('text') for entry in entry_fields.values()]
        new_values.append(status_var.get())

        # Update the treeview with new values
        self.outpass_tree.item(selected_item, values=new_values)

        # Close the pop-up window
        edit_window.destroy()

# Example of usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Admin Outpass Management")
    admin_outpass = AdminOutpass(root)
    admin_outpass.pack(expand=True, fill='both')
    root.mainloop()
