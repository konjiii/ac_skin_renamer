import tkinter as tk
import os
import pickle
from backend.file_io_functions import valid_path, get_settings
from backend import SkinManager
from ui import PathInputFrame, ControlFrame, SkinDisplayFrame

class SkinRenamerApp(tk.Frame):
    """Main application class."""
    def __init__(self, parent, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Skin Renamer")
        self.parent.geometry("800x600")
        self.parent.minsize(600, 400)

        self.settings = get_settings()
        self.AC_PATH = self.settings.get("AC_PATH")

        if not valid_path(self.AC_PATH):
            self.path_input_frame = PathInputFrame(self.parent, self)
            self.path_input_frame.pack(expand=True)
        else:
            self.initialize_main_app()

    def initialize_main_app(self) -> None:
        # backend manager
        self.skin_manager = SkinManager(self)

        # UI components
        self.control_frame = ControlFrame(self.parent, self.skin_manager)
        self.control_frame.pack(fill="x")

        self.skin_display_frame = SkinDisplayFrame(self.parent, self.skin_manager, text="Select Skin")
        self.skin_display_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.control_frame.set_skin_display_frame(self.skin_display_frame)

        # Initial data load
        self.skin_manager.update_data()
        self.skin_display_frame.render_renames()

if __name__ == "__main__":
    if not os.path.exists("settings.pkl"):
        with open("settings.pkl", "wb") as f:
            pickle.dump({"AC_PATH": None}, f)

    root = tk.Tk()
    app = SkinRenamerApp(root)
    root.mainloop()
