import tkinter as tk
from tkinter import ttk, simpledialog as sd
from file_io_functions import save_ror_names
from htmlparser import rorSkinParser

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
