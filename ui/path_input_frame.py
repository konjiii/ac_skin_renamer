import tkinter as tk
from tkinter import ttk, filedialog as fd
import os
import sys
from backend.file_io_functions import valid_path, save_ac_path


class PathInputFrame(ttk.Frame):
    """Frame for handling the Assetto Corsa path input."""

    def __init__(self, parent, app, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.parent = parent
        self.create_widgets()

    def create_widgets(self) -> None:
        self.ac_path_var = tk.StringVar(value="Input Assetto Corsa directory")
        ac_path_input = ttk.Entry(self, textvariable=self.ac_path_var, width=50)
        ac_path_input.pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        browse_button = ttk.Button(
            button_frame, text="Browse", command=self.browse_ac_path
        )
        browse_button.pack(side="left", padx=5)

        accept_button = ttk.Button(
            button_frame, text="Accept", command=self.accept_ac_path
        )
        accept_button.pack(side="left", padx=5)

    def browse_ac_path(self) -> None:
        directory = fd.askdirectory(title="Select Assetto Corsa directory")
        if directory:
            self.app.settings["AC_PATH"] = directory
            self.ac_path_var.set(directory)

    def accept_ac_path(self) -> None:
        if not valid_path(self.app.settings["AC_PATH"]):
            print("Invalid path")
            return

        # Save the new path to settings.pkl
        save_ac_path(self.app.settings)

        # Restart the app to re-initialize with the new path
        self.app.parent.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)
