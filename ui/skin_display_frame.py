import tkinter as tk
from tkinter import ttk

class SkinDisplayFrame(ttk.LabelFrame):
    """Frame for displaying and managing skin renames."""
    def __init__(self, parent, skin_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.skin_manager = skin_manager
        self.canvas_frame = None
        self.create_widgets()

    def create_widgets(self):
        # renames frame
        self.renames_frame = ttk.Frame(self)
        self.renames_frame.pack(fill="both", expand=True, padx=10, pady=5)
        # fix problems with resizing window
        self.renames_frame.pack_propagate(False)

        # canvas where the renames are shown
        self.renames_canvas = tk.Canvas(self.renames_frame)
        self.renames_canvas.pack(side="left", fill="both", expand=True)

        # scrollbar to scroll through the canvas
        scrollbar = ttk.Scrollbar(self.renames_frame, orient="vertical", command=self.renames_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.renames_canvas.configure(yscrollcommand=scrollbar.set)

        # buttons to apply or reset changes
        button_frame = ttk.Frame(self)
        button_frame.pack(side="bottom", fill="x", pady=5)

        apply_button = ttk.Button(button_frame, text="Apply Changes", command=self.skin_manager.apply_changes)
        apply_button.pack(side="left", padx=10)

        reset_button = ttk.Button(button_frame, text="Reset Changes", command=self.skin_manager.reset_changes)
        reset_button.pack(side="left", padx=10)

    def render_renames(self):
        # Clear previous widgets
        if self.canvas_frame:
            self.canvas_frame.destroy()

        # Create a new frame inside the canvas
        self.canvas_frame = ttk.Frame(self.renames_canvas)
        # Create a window for the canvas frame
        canvas_window = self.renames_canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        if not self.skin_manager.ror_names:
            no_ror_label = ttk.Label(self.canvas_frame, text="No ROR names found. Please add ROR names.")
            no_ror_label.pack(padx=10, pady=10)
            return

        # this function handles mouse wheel scrolling
        def on_mousewheel(event):
            # /120 to get 1 unit per notch
            self.renames_canvas.yview_scroll(int(-event.delta/120), "units")

            # Prevent default scrolling behavior of widgets
            return "break"

        # Render each ROR name with a corresponding skin selection combobox
        for ror_name in self.skin_manager.ror_names:
            skin_frame = ttk.Frame(self.canvas_frame)
            skin_frame.pack(fill="x", padx=10, pady=5)

            skin_combobox = ttk.Combobox(skin_frame, values=self.skin_manager.skins)
            skin_combobox.pack(side="left", padx=(0, 10))

            ror_name_label = ttk.Label(skin_frame, text=ror_name)
            ror_name_label.pack(side="left")

            # Bind mouse wheel scrolling
            skin_frame.bind("<MouseWheel>", on_mousewheel)
            skin_combobox.unbind
            skin_combobox.bind("<MouseWheel>", on_mousewheel)
            ror_name_label.bind("<MouseWheel>", on_mousewheel)

            # Update skin dict when selection changes
            skin_combobox.bind("<<ComboboxSelected>>", 
                lambda event, ror=ror_name, combo=skin_combobox: 
                self.skin_manager.update_skin_mapping(ror, combo.get())
            )

            self.skin_manager.rename_comboboxes[ror_name] = skin_combobox

        self.canvas_frame.update_idletasks()
        # Update scrollregion
        self.renames_canvas.configure(scrollregion=self.renames_canvas.bbox("all"))

        def configure_canvas_frame(event):
            self.renames_canvas.itemconfig(canvas_window, width=event.width)
        
        self.renames_canvas.bind('<Configure>', configure_canvas_frame)
        # Bind mouse wheel scrolling
        self.renames_canvas.bind("<MouseWheel>", on_mousewheel)
        self.canvas_frame.bind("<MouseWheel>", on_mousewheel)
