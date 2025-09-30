import tkinter as tk
from tkinter import ttk
import os
import pickle
from helper_functions import valid_path, get_settings
from file_io_functions import get_cars, get_skins, get_ror_names
from ui.path_input_frame import PathInputFrame
from ui.control_frame import ControlFrame
from ui.skin_display_frame import SkinDisplayFrame

class SkinRenamerApp(tk.Frame):
    """Main application class."""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Skin Renamer")
        self.parent.geometry("800x600")

        self.settings = get_settings()
        self.AC_PATH = self.settings.get("AC_PATH")

        if not valid_path(self.AC_PATH):
            self.path_input_frame = PathInputFrame(self.parent, self)
            self.path_input_frame.pack(expand=True)
        else:
            self.initialize_main_app()

    def initialize_main_app(self):
        self.cars = get_cars(self.AC_PATH)
        self.skins = []
        self.ror_names = []

        self.control_frame = ControlFrame(self.parent, self)
        self.control_frame.pack(fill="x")

        self.skin_display_frame = SkinDisplayFrame(self.parent, self, text="Select Skin")
        self.skin_display_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Initial data load
        self.update_data()

    def update_data(self):
        """Update skins and ror_names based on the selected car and re-render."""
        selected_car = self.control_frame.car_combobox.get()
        if not selected_car:
            return
            
        self.skins = get_skins(self.AC_PATH, selected_car)
        self.ror_names = get_ror_names(self.AC_PATH, selected_car)
        self.skin_display_frame.render_renames()

if __name__ == "__main__":
    if not os.path.exists("settings.pkl"):
        with open("settings.pkl", "wb") as f:
            pickle.dump({"AC_PATH": None}, f)

    root = tk.Tk()
    app = SkinRenamerApp(root)
    root.mainloop()
