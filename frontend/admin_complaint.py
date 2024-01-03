import tkinter as tk
from tkinter import ttk, Button, Toplevel, Label, Text, StringVar, messagebox
import mysql.connector
from config import db_config_manager

class AdminComplaint(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.create_widgets()
        self.fetch_complaints_from_db()

    def create_widgets(self):
        # Create a frame to center the treeview
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        Label(center_frame, text='Complaints Record (Double click to update status)', font=('Microsoft YaHei UI Light', 20, 'bold'), bg='white', fg = 'black').pack(pady=30)

        # Create a treeview for displaying complaints
        columns = ('CID', 'CMS', 'Date', 'Complaint Detail', 'Status')
        self.complaint_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        # Set column headings
        for col in columns:
            self.complaint_tree.heading(col, text=col)

        # Set column widths
        self.complaint_tree.column('CID', width=80)
        self.complaint_tree.column('CMS', width=80)
        self.complaint_tree.column('Date', width=120)
        self.complaint_tree.column('Complaint Detail', width=300)
        self.complaint_tree.column('Status', width=80)

        self.complaint_tree.pack(padx=20, pady=40, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.complaint_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.complaint_tree.configure(yscrollcommand=scrollbar.set)

        # Bind double click on treeview item to show complaint details
        self.complaint_tree.bind("<Double-1>", self.show_complaint_details)

    def fetch_complaints_from_db(self):
        try:
            connection = mysql.connector.connect(**db_config_manager)
            cursor = connection.cursor()

            query = "SELECT CID, CMS, CDate, CDescription, CStatus FROM Complaint"
            cursor.execute(query)
            complaints_data = cursor.fetchall()

            # Clear existing items in the treeview
            self.complaint_tree.delete(*self.complaint_tree.get_children())

            # Insert new data into the treeview
            for complaint in complaints_data:
                self.complaint_tree.insert('', 'end', values=complaint)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching complaints: {e}")

        finally:
            if connection:
                connection.close()

    def show_complaint_details(self, event):
        selected_item = self.complaint_tree.selection()

        if not selected_item:
            return

        item_values = self.complaint_tree.item(selected_item)['values']
        cid, cms, date, complaint_detail, status = item_values

        edit_window = Toplevel(self.master)
        edit_window.title('Edit Complaint Details')

        tk.Label(edit_window, text='CID:').grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(edit_window, state='readonly', textvariable=StringVar(value=cid)).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='CMS:').grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(edit_window, state='readonly', textvariable=StringVar(value=cms)).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='Date:').grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(edit_window, state='readonly', textvariable=StringVar(value=date)).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='Complaint Detail:').grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(edit_window, state='readonly', textvariable=StringVar(value=complaint_detail)).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(edit_window, text='Status:').grid(row=4, column=0, padx=10, pady=5)
        status_var = StringVar(value=status)
        status_entry = ttk.Combobox(edit_window, textvariable=status_var, values=['Pending', 'Resolved'])
        status_entry.grid(row=4, column=1, padx=10, pady=5)

        save_button = Button(edit_window, text='Save', command=lambda: self.save_complaint_details(edit_window, selected_item, status_var.get()))
        save_button.grid(row=5, column=1, pady=10)

    def save_complaint_details(self, edit_window, selected_item, new_status):
        item_values = self.complaint_tree.item(selected_item)['values']
        cid, cms, date, complaint_detail, _ = item_values

        try:
            connection = mysql.connector.connect(**db_config_manager)
            cursor = connection.cursor()

            update_query = "UPDATE Complaint SET CStatus = %s WHERE CID = %s"
            cursor.execute(update_query, (new_status, cid))

            connection.commit()

            # Update the treeview with new status
            self.complaint_tree.item(selected_item, values=(cid, cms, date, complaint_detail, new_status))

            messagebox.showinfo("Success", "Complaint details updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating complaint details: {e}")

        finally:
            if connection:
                connection.close()
                edit_window.destroy()

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Admin Complaint Management")
    admin_complaint = AdminComplaint(app)
    app.mainloop()
