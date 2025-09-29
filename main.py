import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import os
import pickle
from helper_functions import valid_path, get_settings
import sys
from file_io_functions import get_cars, get_skins
# import ctypes as ct

# create settings.pkl if it doesn't exist
if not os.path.exists("settings.pkl"):
    with open("settings.pkl", "wb") as f:
        pickle.dump({"AC_PATH": None}, f)


class skinRenamer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.resizable(True, True)
        self.parent.title("Skin Renamer")
        self.parent.geometry("800x600")

        # initialize
        self.settings = get_settings()
        self.AC_PATH = self.settings["AC_PATH"]
        print(self.settings)
        if not valid_path(self.AC_PATH):
            self.create_path_input()
            return

        # create the GUI
        # list of cars
        self.cars = get_cars(self.AC_PATH)

        self.select_car_frame = ttk.LabelFrame(self.parent, text="Select Car")
        self.select_car_frame.grid(row=1, column=0, padx=10, pady=10)

        # car selection box
        self.car_combobox = ttk.Combobox(self.select_car_frame)
        self.car_combobox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.car_combobox['values'] = self.cars
        self.car_combobox.bind("<<ComboboxSelected>>", self.update_skins)
        
        # list of skins
        self.skins = get_skins(self.AC_PATH, self.car_combobox.get())

        # skin selection box
        self.select_skin_frame = ttk.LabelFrame(self.parent, text="Select Skin")
        self.select_skin_frame.grid(row=3, column=0, padx=10, pady=10)

        # list of renames
        self.renames = list()
        self.add_rename()
        self.render_renames()

        # button to add a rename to list of renames
        self.add_skin_rename_button = ttk.Button(self.parent, text="+", command=self.add_rename)
        self.add_skin_rename_button.grid(row=2, column=0, padx=10, pady=10)


    def create_path_input(self):
        # ask user to set path to AC
        self.ac_path_var = tk.StringVar(value="Input Assetto Corsa directory")
        self.ac_path_input = ttk.Entry(self.parent, textvariable=self.ac_path_var, width=50)
        self.ac_path_input.grid(row=0, column=0, columnspan=2, padx=self.parent.winfo_width(), pady=self.parent.winfo_height())

        self.dir_accept_button = ttk.Button(self.parent, text="Browse", command=self.browse_ac_path)
        self.dir_accept_button.grid(row=1, column=0, padx=10, pady=10)

        self.dir_accept_button = ttk.Button(self.parent, text="Accept", command=self.accept_ac_path)
        self.dir_accept_button.grid(row=1, column=1, padx=10, pady=10)

    def browse_ac_path(self):
        directory = fd.askdirectory(title="Select Assetto Corsa directory")
        self.settings["AC_PATH"] = directory
        self.ac_path_var.set(directory)

    def accept_ac_path(self):
        if not valid_path(self.settings["AC_PATH"]):
            print("Invalid path")
            return
        with open("settings.pkl", "wb") as f:
            pickle.dump(self.settings, f)
        self.ac_path_input.destroy()
        self.dir_accept_button.destroy()
        self.dir_accept_button.destroy()
        # restart the app
        root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    def update_skins(self, _):
        """
        update self.skins list for the selected car
        """
        self.skins = get_skins(self.AC_PATH, self.car_combobox.get())
        for skin_combobox, _ in self.renames:
            skin_combobox['values'] = self.skins
            skin_combobox.set('')

    def add_rename(self):
        """
        Add a new skin rename row
        """
        skin_combobox = ttk.Combobox(self.select_skin_frame)
        skin_combobox['values'] = self.skins

        skin_names = ["Default", "Skin1", "Skin2", "Skin3", "Skin4", "Skin5"]
        rename_combobox = ttk.Combobox(self.select_skin_frame)
        rename_combobox['values'] = skin_names
        self.renames.append((skin_combobox, rename_combobox))

        self.render_renames()

    def render_renames(self):
        """
        Render all widgets in self.renames
        """
        for i, (skin_combobox, rename_combobox) in enumerate(self.renames):
            skin_combobox.grid(row=3+i, column=0, columnspan=2, padx=10, pady=10)
            rename_combobox.grid(row=3+i, column=2, columnspan=2, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = skinRenamer(root)
    root.mainloop()