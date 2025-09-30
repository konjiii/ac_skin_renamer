import tkinter as tk
from tkinter import ttk, simpledialog as sd, filedialog as fd
import os
import pickle
from helper_functions import valid_path, get_settings
import sys
from file_io_functions import get_cars, get_skins, get_ror_names, save_ror_names
from htmlparser import rorSkinParser

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
        self.select_car_frame.pack(padx=10, pady=10, fill="x")

        # car selection box
        self.car_combobox = ttk.Combobox(self.select_car_frame, values=self.cars)
        self.car_combobox.pack(padx=10, pady=10)
        self.car_combobox.bind("<<ComboboxSelected>>", self.update_skins)
        self.car_combobox.bind("<KeyRelease>", self.update_car_suggestions)

        # list of skins
        self.skins = get_skins(self.AC_PATH, self.car_combobox.get())

        # list of ror skin names
        self.ror_names = get_ror_names(self.AC_PATH, self.car_combobox.get())

        # button frame for add/remove ror names
        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(padx=10, pady=10)

        # button to add or remove ror names
        add_ror_names_button = ttk.Button(self.button_frame, text="Add ROR Names", command=self.add_ror_names)
        add_ror_names_button.pack(side="left", padx=10, pady=10)
        remove_ror_names_button = ttk.Button(self.button_frame, text="Remove ROR Names", command=self.remove_ror_names)
        remove_ror_names_button.pack(side="left", padx=10, pady=10)

        # skin selection box
        self.select_skin_frame = ttk.LabelFrame(self.parent, text="Select Skin")
        self.select_skin_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # select first car as default
        self.car_combobox.current(0)
        self.update_skins(None)


    def update_car_suggestions(self, _) -> None:
        """
        Update the car combobox with suggestions based on what the user has typed.
        """
        typed_text = self.car_combobox.get()

        if typed_text == "":
            self.car_combobox['values'] = self.cars
            return

        suggestions = [car for car in self.cars if typed_text.lower() in car.lower()]
        if suggestions:
            self.car_combobox['values'] = suggestions
        else:
            # Keep the full list if there are no matches
            self.car_combobox['values'] = self.cars


    def create_path_input(self) -> None:
        # ask user to set path to AC
        self.ac_path_var = tk.StringVar(value="Input Assetto Corsa directory")
        self.ac_path_input = ttk.Entry(self.parent, textvariable=self.ac_path_var, width=50)
        self.ac_path_input.pack(padx=10, pady=10)

        self.dir_accept_button = ttk.Button(self.parent, text="Browse", command=self.browse_ac_path)
        self.dir_accept_button.pack(side="left", padx=10, pady=10)

        self.dir_accept_button = ttk.Button(self.parent, text="Accept", command=self.accept_ac_path)
        self.dir_accept_button.pack(side="left", padx=10, pady=10)

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

        # show error if no ror names found
        if not self.ror_names:
            no_ror_label = ttk.Label(self.select_skin_frame, text="No ROR names found. Please add ROR names.")
            no_ror_label.pack(padx=10, pady=10)
            return
        
        # scrollable canvas where the renames will be rendered
        renames_canvas = tk.Canvas(self.select_skin_frame, width=600, height=300)
        renames_canvas.pack(side="left", fill="both", expand=True)
        
        # scrollbar for canvas
        scrollbar = ttk.Scrollbar(self.select_skin_frame, orient="vertical", command=renames_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        renames_canvas.configure(yscrollcommand=scrollbar.set)

        # create a frame inside the canvas to hold all the widgets
        canvas_frame = ttk.Frame(renames_canvas)
        canvas_window = renames_canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        # render rename widget for every ror skin name
        for skin in enumerate(self.ror_names):
            # create a frame for each skin pair
            skin_frame = ttk.Frame(canvas_frame)
            skin_frame.pack(fill="x", padx=10, pady=5)
            
            skin_combobox = ttk.Combobox(skin_frame, values=self.skins)
            skin_combobox.pack(side="left", padx=(0, 10))

            ror_name = ttk.Label(skin_frame, text=skin[1])
            ror_name.pack(side="left")

        # update the canvas scroll region after all widgets are added
        canvas_frame.update_idletasks()
        renames_canvas.configure(scrollregion=renames_canvas.bbox("all"))
        
        # configure the canvas window to expand with the canvas width
        def configure_canvas_frame(event):
            canvas_width = event.width
            renames_canvas.itemconfig(canvas_window, width=canvas_width)
        
        renames_canvas.bind('<Configure>', configure_canvas_frame)
        
        # bind mouse wheel scrolling to the canvas
        def on_mousewheel(event):
            renames_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        renames_canvas.bind("<MouseWheel>", on_mousewheel)
        canvas_frame.bind("<MouseWheel>", on_mousewheel)

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