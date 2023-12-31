import tkinter as tk
from tkinter import ttk, Scrollbar, Button, Toplevel, Label, StringVar
import mysql.connector
from config import db_config_manager

class AdminOutpass(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.create_widgets()
        self.fetch_outpasses_from_db()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        columns = ('OID', 'Leaving Date', 'Joining Date', 'Purpose', 'Status', 'Student CMS', 'Guardian 1', 'Guardian 2', 'Guardian 3')
        self.outpass_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        for col in columns:
            self.outpass_tree.heading(col, text=col)

        for col in columns[1:]:
            self.outpass_tree.column(col, width=100)

        self.outpass_tree.pack(padx=20, pady=40, side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(center_frame, orient='vertical', command=self.outpass_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.outpass_tree.configure(yscrollcommand=scrollbar.set)

        self.outpass_tree.bind('<Double-1>', self.edit_outpass_details)

    def fetch_outpasses_from_db(self):
        try:
            connection = mysql.connector.connect(**db_config_manager)
            cursor = connection.cursor()

            query = """
                SELECT o.OID, o.LeavingDate, o.JoiningDate, o.Purpose, o.OStatus, o.cms, g1.gName AS Guardian1, g2.gName AS Guardian2, g3.gName AS Guardian3
                FROM Outpass o
                LEFT JOIN Guardian g1 ON o.cms = g1.cms
                LEFT JOIN Guardian g2 ON o.cms = g2.cms
                LEFT JOIN Guardian g3 ON o.cms = g3.cms
            """

            cursor.execute(query)
            outpasses_data = cursor.fetchall()

            self.outpass_tree.delete(*self.outpass_tree.get_children())

            for outpass in outpasses_data:
                oid, leaving_date, joining_date, purpose, status, student_cms, guardian1, guardian2, guardian3 = outpass
                values = (oid, str(leaving_date), str(joining_date), purpose, status, student_cms, guardian1, guardian2, guardian3)
                self.outpass_tree.insert('', 'end', values=values)

        except mysql.connector.Error as e:
            print(f"Error fetching outpasses: {e}")

        finally:
            if connection:
                connection.close()

    def edit_outpass_details(self, event):
        selected_item = self.outpass_tree.selection()[0]
        edit_window = Toplevel(self)
        edit_window.title('Edit Outpass Details')

        item_values = self.outpass_tree.item(selected_item, 'values')

        labels = ['Purpose', 'Leaving Date', 'Joining Date', 'Guardian 1 Contact', 'Guardian 2 Contact', 'Guardian 3 Contact']

        entry_fields = {}
        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).grid(row=i, column=0, pady=5, padx=5)
            entry = Label(edit_window, text=str(item_values[i + 3]))
            entry.grid(row=i, column=1, pady=5, padx=5)
            entry_fields[label] = entry

        status_var = StringVar(edit_window)
        status_var.set(item_values[4])
        status_label = tk.Label(edit_window, text='Status')
        status_label.grid(row=len(labels), column=0, pady=5, padx=5)
        status_menu = ttk.Combobox(edit_window, textvariable=status_var, values=['Pending', 'Approved', 'Rejected'])
        status_menu.grid(row=len(labels), column=1, pady=5, padx=5)

        save_button = Button(edit_window, text='Save', command=lambda: self.save_outpass_details(edit_window, selected_item, entry_fields, status_var))
        save_button.grid(row=len(labels) + 1, columnspan=2, pady=10)

    def save_outpass_details(self, edit_window, selected_item, entry_fields, status_var):
        oid = selected_item.split()[0]
        existing_values = list(self.outpass_tree.item(selected_item, 'values'))
        existing_values[4] = status_var.get()
        self.outpass_tree.item(selected_item, values=existing_values)
        new_status = status_var.get()
        self.update_outpass_status_in_db(oid, new_status)
        edit_window.destroy()

    def update_outpass_status_in_db(self, oid, new_status):
        if new_status != "Pending":
            print("Status can only be updated to 'Pending'.")
            return

        try:
            connection = mysql.connector.connect(**db_config_manager)
            cursor = connection.cursor()

            oid = int(oid)

            # Update the status only if it's currently 'Pending'
            update_query = "UPDATE Outpass SET OStatus = %s WHERE OID = %s AND OStatus = 'Pending'"
            cursor.execute(update_query, (new_status, oid))

            connection.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                print("Outpass status updated successfully!")
            else:
                print(f"No Outpass with matching OID {oid} and Pending status found or the status is already {new_status}.")

        except mysql.connector.Error as e:
            print(f"Error updating outpass status: {e}")

        finally:
            if connection:
                connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Admin Outpass Management")
    admin_outpass = AdminOutpass(root)
    admin_outpass.pack(expand=True, fill='both')
    root.mainloop()
