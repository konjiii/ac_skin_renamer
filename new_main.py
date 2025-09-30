import tkinter as tk
from tkinter import ttk, simpledialog as sd, filedialog as fd
import os
import pickle
import sys
from helper_functions import valid_path, get_settings
from file_io_functions import get_cars, get_skins, get_ror_names, save_ror_names
from htmlparser import rorSkinParser

class PathInputFrame(ttk.Frame):
    """Frame for handling the Assetto Corsa path input."""
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.ac_path_var = tk.StringVar(value="Input Assetto Corsa directory")
        ac_path_input = ttk.Entry(self, textvariable=self.ac_path_var, width=50)
        ac_path_input.pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        browse_button = ttk.Button(button_frame, text="Browse", command=self.browse_ac_path)
        browse_button.pack(side="left", padx=5)

        accept_button = ttk.Button(button_frame, text="Accept", command=self.accept_ac_path)
        accept_button.pack(side="left", padx=5)

    def browse_ac_path(self):
        directory = fd.askdirectory(title="Select Assetto Corsa directory")
        if directory:
            self.app.settings["AC_PATH"] = directory
            self.ac_path_var.set(directory)

    def accept_ac_path(self):
        if not valid_path(self.app.settings["AC_PATH"]):
            print("Invalid path")
            return
        with open("settings.pkl", "wb") as f:
            pickle.dump(self.app.settings, f)
        
        # Restart the app to re-initialize with the new path
        self.app.parent.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

class ControlFrame(ttk.Frame):
    """Frame for car selection and ROR name management."""
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Car selection
        select_car_frame = ttk.LabelFrame(self, text="Select Car")
        select_car_frame.pack(padx=10, pady=10, fill="x")

        self.car_combobox = ttk.Combobox(select_car_frame, values=self.app.cars)
        self.car_combobox.pack(padx=10, pady=10)
        self.car_combobox.bind("<<ComboboxSelected>>", self.update_selection)
        self.car_combobox.bind("<KeyRelease>", self.update_car_suggestions)
        if self.app.cars:
            self.car_combobox.current(0)

        # ROR names buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        add_ror_names_button = ttk.Button(button_frame, text="Add ROR Names", command=self.add_ror_names)
        add_ror_names_button.pack(side="left", padx=10)
        remove_ror_names_button = ttk.Button(button_frame, text="Remove ROR Names", command=self.remove_ror_names)
        remove_ror_names_button.pack(side="left", padx=10)

    def update_selection(self, _):
        self.app.update_data()

    def update_car_suggestions(self, _):
        typed_text = self.car_combobox.get()
        if not typed_text:
            self.car_combobox['values'] = self.app.cars
            return
        
        suggestions = [car for car in self.app.cars if typed_text.lower() in car.lower()]
        if suggestions:
            self.car_combobox['values'] = suggestions
        else:
            self.car_combobox['values'] = self.app.cars

    def add_ror_names(self):
        ror_html = sd.askstring("Input", "Paste ROR skin names HTML here:")
        if not ror_html:
            return
        
        parser = rorSkinParser()
        parser.feed(ror_html)
        self.app.ror_names = parser.ror_skins
        
        if save_ror_names(self.app.AC_PATH, self.car_combobox.get(), self.app.ror_names) == -1:
            print("Error saving ror names")
        
        self.app.update_data()

    def remove_ror_names(self):
        self.app.ror_names = []
        if save_ror_names(self.app.AC_PATH, self.car_combobox.get(), self.app.ror_names) == -1:
            print("Error removing ror names")
        
        self.app.update_data()

class SkinDisplayFrame(ttk.LabelFrame):
    """Frame for displaying and managing skin renames."""
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.canvas_frame = None
        self.create_widgets()

    def create_widgets(self):
        self.renames_canvas = tk.Canvas(self, width=600, height=300)
        self.renames_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.renames_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.renames_canvas.configure(yscrollcommand=scrollbar.set)

    def render_renames(self):
        # Clear previous widgets
        if self.canvas_frame:
            self.canvas_frame.destroy()

        self.canvas_frame = ttk.Frame(self.renames_canvas)
        canvas_window = self.renames_canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        if not self.app.ror_names:
            no_ror_label = ttk.Label(self.canvas_frame, text="No ROR names found. Please add ROR names.")
            no_ror_label.pack(padx=10, pady=10)
            return

        for skin_name in self.app.ror_names:
            skin_frame = ttk.Frame(self.canvas_frame)
            skin_frame.pack(fill="x", padx=10, pady=5)
            
            skin_combobox = ttk.Combobox(skin_frame, values=self.app.skins)
            skin_combobox.pack(side="left", padx=(0, 10))

            ror_name_label = ttk.Label(skin_frame, text=skin_name)
            ror_name_label.pack(side="left")

        self.canvas_frame.update_idletasks()
        self.renames_canvas.configure(scrollregion=self.renames_canvas.bbox("all"))

        def configure_canvas_frame(event):
            self.renames_canvas.itemconfig(canvas_window, width=event.width)
        
        def on_mousewheel(event):
            self.renames_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.renames_canvas.bind('<Configure>', configure_canvas_frame)
        self.renames_canvas.bind("<MouseWheel>", on_mousewheel)
        self.canvas_frame.bind("<MouseWheel>", on_mousewheel)

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
