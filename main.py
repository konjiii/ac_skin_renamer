import tkinter as tk
from tkinter import ttk, simpledialog as sd, filedialog as fd
import os
import pickle
from helper_functions import valid_path, get_settings
import sys
from file_io_functions import get_cars, get_skins, get_ror_names, save_ror_names
from htmlparser import rorSkinParser
# import ctypes as ct

# create settings.pkl if it doesn't exist
if not os.path.exists("settings.pkl"):
    with open("settings.pkl", "wb") as f:
        pickle.dump({"AC_PATH": None}, f)


class skinRenamer(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
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
        self.select_car_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # car selection box
        self.car_combobox = ttk.Combobox(self.select_car_frame)
        self.car_combobox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.car_combobox['values'] = self.cars
        self.car_combobox.bind("<<ComboboxSelected>>", self.update_skins)

        # button to add or remove ror names
        add_ror_names_button = ttk.Button(self.parent, text="Add ROR Names", command=self.add_ror_names)
        add_ror_names_button.grid(row=1, column=0, padx=10, pady=10)
        remove_ror_names_button = ttk.Button(self.parent, text="Remove ROR Names", command=self.remove_ror_names)
        remove_ror_names_button.grid(row=1, column=1, padx=10, pady=10)

        # list of skins
        self.skins = get_skins(self.AC_PATH, self.car_combobox.get())

        # list of ror skin names
        self.ror_names = get_ror_names(self.AC_PATH, self.car_combobox.get())

        # skin selection box
        self.select_skin_frame = ttk.LabelFrame(self.parent, text="Select Skin")
        self.select_skin_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # select first car as default
        self.car_combobox.current(0)
        self.update_skins(None)


    def create_path_input(self) -> None:
        # ask user to set path to AC
        self.ac_path_var = tk.StringVar(value="Input Assetto Corsa directory")
        self.ac_path_input = ttk.Entry(self.parent, textvariable=self.ac_path_var, width=50)
        self.ac_path_input.grid(row=0, column=0, columnspan=2, padx=self.parent.winfo_width(), pady=self.parent.winfo_height())

        self.dir_accept_button = ttk.Button(self.parent, text="Browse", command=self.browse_ac_path)
        self.dir_accept_button.grid(row=1, column=0, padx=10, pady=10)

        self.dir_accept_button = ttk.Button(self.parent, text="Accept", command=self.accept_ac_path)
        self.dir_accept_button.grid(row=1, column=1, padx=10, pady=10)

    def browse_ac_path(self) -> None:
        directory = fd.askdirectory(title="Select Assetto Corsa directory")
        self.settings["AC_PATH"] = directory
        self.ac_path_var.set(directory)

    def accept_ac_path(self) -> None:
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

    def update_skins(self, _) -> None:
        """
        update skins and ror_names when a car is selected
        """
        self.skins = get_skins(self.AC_PATH, self.car_combobox.get())
        self.ror_names = get_ror_names(self.AC_PATH, self.car_combobox.get())
        self.render_renames()

    def render_renames(self) -> None:
        """
        Render all widgets in self.renames
        """

        # clear previous widgets in select_skin_frame
        for widget in self.select_skin_frame.winfo_children():
            widget.destroy()

        # render rename widget for every ror skin name
        for skin in enumerate(self.ror_names):
            skin_combobox = ttk.Combobox(self.select_skin_frame)
            skin_combobox['values'] = self.skins
            skin_combobox.grid(row=skin[0]+1, column=0, padx=10, pady=10)

            ror_name = ttk.Label(self.select_skin_frame, text=skin[1])
            ror_name.grid(row=skin[0]+1, column=1, padx=10, pady=10)

    def add_ror_names(self) -> None:
        """
        parse html from ROR skin names page and add to self.ror_names
        """
        # ask user to paste html from ROR skin names page
        ror_html = sd.askstring("Input", "Paste ROR skin names HTML here:")
        if ror_html is None:
            return
        
        # initialize parser and parse html
        parser = rorSkinParser()
        parser.feed(ror_html)
        self.ror_names = parser.ror_skins

        # save ror_names
        code = save_ror_names(self.AC_PATH, self.car_combobox.get(), self.ror_names)

        if code == -1:
            print("Error saving ror names")
            return

        # rerender the renames section
        self.render_renames()

    def remove_ror_names(self) -> None:
        """
        remove all ror names
        """
        self.ror_names = []
        code = save_ror_names(self.AC_PATH, self.car_combobox.get(), self.ror_names)

        if code == -1:
            print("Error saving ror names")
            return

        # rerender the renames section
        self.render_renames()

if __name__ == "__main__":
    root = tk.Tk()
    app = skinRenamer(root)
    root.mainloop()