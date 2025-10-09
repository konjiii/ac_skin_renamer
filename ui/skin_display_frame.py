import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as sd


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
        scrollbar = ttk.Scrollbar(
            self.renames_frame, orient="vertical", command=self.renames_canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.renames_canvas.configure(yscrollcommand=scrollbar.set)

        # buttons to apply or reset changes and copy/paste configuration
        button_frame = ttk.Frame(self)
        button_frame.pack(side="bottom", fill="x", pady=5)

        apply_button = ttk.Button(
            button_frame, text="Apply Changes", command=self.skin_manager.apply_changes
        )
        apply_button.pack(side="left", padx=10)

        reset_button = ttk.Button(
            button_frame, text="Reset Changes", command=self.skin_manager.reset_changes
        )
        reset_button.pack(side="left", padx=10)

        paste_button = ttk.Button(
            button_frame,
            text="Paste configuration",
            command=self.paste_dialog,
        )
        paste_button.pack(side="right", padx=10)

        self.copy_button = ttk.Button(
            button_frame,
            text="Copy configuration",
            command=self.copy_handler,
            width=20,
        )
        self.copy_button.pack(side="right", padx=10)

        self.copy_button_timer = None

    def render_renames(self):
        # Clear previous widgets
        if self.canvas_frame:
            self.canvas_frame.destroy()

        # Create a new frame inside the canvas
        self.canvas_frame = ttk.Frame(self.renames_canvas)
        # Create a window for the canvas frame
        canvas_window = self.renames_canvas.create_window(
            (0, 0), window=self.canvas_frame, anchor="nw"
        )

        if not self.skin_manager.ror_names:
            no_ror_label = ttk.Label(
                self.canvas_frame, text="No ROR names found. Please add ROR names."
            )
            no_ror_label.pack(padx=10, pady=10)
            return

        # this function handles mouse wheel scrolling
        def on_mousewheel(event):
            # /120 to get 1 unit per notch
            self.renames_canvas.yview_scroll(int(-event.delta / 120), "units")

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

            # set current selection if already mapped
            if ror_name in self.skin_manager.renames:
                skin_combobox.set(self.skin_manager.renames[ror_name])

            # Bind mouse wheel scrolling
            skin_frame.bind("<MouseWheel>", on_mousewheel)
            skin_combobox.unbind
            skin_combobox.bind("<MouseWheel>", on_mousewheel)
            ror_name_label.bind("<MouseWheel>", on_mousewheel)

            # Update skin dict when selection changes
            skin_combobox.bind(
                "<<ComboboxSelected>>",
                lambda event,
                ror=ror_name,
                combo=skin_combobox: self.skin_manager.update_skin_mapping(
                    ror, combo.get()
                ),
            )

            self.skin_manager.rename_comboboxes[ror_name] = skin_combobox

        self.canvas_frame.update_idletasks()
        # Update scrollregion
        self.renames_canvas.configure(scrollregion=self.renames_canvas.bbox("all"))

        def configure_canvas_frame(event):
            self.renames_canvas.itemconfig(canvas_window, width=event.width)

        self.renames_canvas.bind("<Configure>", configure_canvas_frame)
        # Bind mouse wheel scrolling
        self.renames_canvas.bind("<MouseWheel>", on_mousewheel)
        self.canvas_frame.bind("<MouseWheel>", on_mousewheel)

    def copy_handler(self):
        """
        Handle copy button click, update button text based on success or failure.
        """
        result = self.skin_manager.copy_configuration()
        if result == -1:
            if self.copy_button_timer:
                self.after_cancel(self.copy_button_timer)
            self.copy_button.config(text="No renames to copy...")
            self.copy_button_timer = self.after(1000, lambda: self.copy_button.config(text="Copy configuration"))
        else:
            if self.copy_button_timer:
                self.after_cancel(self.copy_button_timer)
            self.copy_button.config(text="Success!")
            self.copy_button_timer = self.after(1000, lambda: self.copy_button.config(text="Copy configuration"))

    def paste_dialog(self):
        """
        Handle paste dialog, get configuration text from user send to skin manager.
        """
        config_text = sd.askstring("Input", "Paste configuration here:")
        if not config_text:
            return

        self.skin_manager.paste_configuration(config_text)
        self.render_renames()
