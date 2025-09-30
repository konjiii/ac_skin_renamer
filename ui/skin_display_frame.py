import tkinter as tk
from tkinter import ttk

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
