<<<<<<< Updated upstream
=======
# #main.py
# import tkinter as tk
# from frontend.main_window import MainWindow
# from backend.initializeDatabase import initialize_database

# if __name__ == "__main__":
#     print('here')
#     initialize_database()
#     app = MainWindow()
#     app.mainloop()
import os
from config import current_script_path

nhms_folder_path = os.path.dirname(os.path.dirname(current_script_path))
print(nhms_folder_path)
>>>>>>> Stashed changes
