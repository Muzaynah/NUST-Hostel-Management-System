import tkinter as tk
from tkinter import ttk

class AdminNotification(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create a Treeview widget
        self.notification_tree = ttk.Treeview(self, columns=('Date', 'Detail'), show='headings', selectmode='browse')

        # Define column headings
        self.notification_tree.heading('Date', text='Date')
        self.notification_tree.heading('Detail', text='Detail')

        # Set column widths
        self.notification_tree.column('Date', width=150)  # Adjust the width as needed
        self.notification_tree.column('Detail', width=500)  # Adjust the width as needed

        # Add some sample data (you can replace this with your actual data)
        self.notification_tree.insert('', 'end', values=('2023-01-01', 'Notification Detail 1'))
        self.notification_tree.insert('', 'end', values=('2023-01-02', 'Notification Detail 2'))

        # Pack the Treeview widget
        self.notification_tree.pack(padx=10, pady=10, ipady=50)

        # Add a button to open the panel for adding notifications
        add_notification_button = tk.Button(self, text='Add Notification', command=self.show_add_notification_panel)
        add_notification_button.pack(pady=10)

    def show_add_notification_panel(self):
        # Create a new window for adding notifications
        add_notification_window = tk.Toplevel(self.master)
        add_notification_window.title('Add Notification')

        # Create labels, entry fields, and a Save button
        tk.Label(add_notification_window, text='Date:').pack(pady=5)
        date_entry = tk.Entry(add_notification_window)
        date_entry.pack(pady=5)

        tk.Label(add_notification_window, text='Details:').pack(pady=5)
        details_text = tk.Text(add_notification_window, width=40, height=5)
        details_text.pack(pady=5)

        save_button = tk.Button(add_notification_window, text='Save', command=lambda: self.save_notification(add_notification_window, date_entry.get(), details_text.get("1.0", "end-1c")))
        save_button.pack(pady=10)

    def save_notification(self, add_notification_window, date, details):
        # Insert the new notification into the Treeview
        self.notification_tree.insert('', 'end', values=(date, details))
        add_notification_window.destroy()

# Example of usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Admin Notification Management")
    admin_notification = AdminNotification(root, None)
    admin_notification.pack(expand=True, fill='both')
    root.mainloop()
