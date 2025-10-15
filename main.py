import os
import json
from pathlib import Path
import tkinter as tk
from backend.file_io_functions import valid_path, get_settings
from backend import SkinManager
from ui import PathInputFrame, ControlFrame, SkinDisplayFrame
import globals

class SkinRenamerApp(tk.Frame):
    """Main application class."""

    def __init__(self, parent, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Skin Renamer")
        self.parent.geometry("800x600")
        self.parent.minsize(600, 400)

        self.initialize_root()

        self.settings = get_settings()
        AC_PATH = self.settings.get("AC_PATH")
        SAVE_PATH = self.settings.get("SAVE_PATH")

        if not valid_path(AC_PATH):
            self.path_input_frame = PathInputFrame(self.parent, self)
            self.path_input_frame.pack(expand=True)
        else:
            self.AC_PATH = Path(AC_PATH)
            self.SAVE_PATH = Path(SAVE_PATH)
            self.initialize_main_app()

    def initialize_root(self) -> None:
        # ensure saves directory exists
        SAVE_PATH = str(globals.ROOT_DIR / "saves")
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)

        # ensure settings.json exists
        if not os.path.exists(globals.ROOT_DIR / "settings.json"):
            with open(globals.ROOT_DIR / "settings.json", "w") as f:
                json.dump({"AC_PATH": None, "SAVE_PATH": SAVE_PATH}, f)

    def initialize_main_app(self) -> None:
        # backend manager
        self.skin_manager = SkinManager(self.AC_PATH, self.SAVE_PATH)

        # UI components
        self.control_frame = ControlFrame(self.parent, self.skin_manager)
        self.control_frame.pack(fill="x")

        self.skin_display_frame = SkinDisplayFrame(
            self.parent, self.skin_manager, text="Select Skin"
        )
        self.skin_display_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.control_frame.set_skin_display_frame(self.skin_display_frame)

        # Initial data load
        self.skin_manager.update_car_data(self.control_frame.car_combobox.get())
        self.skin_display_frame.render_renames()


if __name__ == "__main__":
    root = tk.Tk()
    app = SkinRenamerApp(root)
    root.mainloop()
