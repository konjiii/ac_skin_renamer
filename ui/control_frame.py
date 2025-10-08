from tkinter import ttk, simpledialog as sd
from backend.file_io_functions import save_ror_names
from backend import RorHTMLParser


class ControlFrame(ttk.Frame):
    """Frame for car selection and ROR name management."""

    def __init__(self, parent, skin_manager, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.skin_manager = skin_manager
        self.AC_PATH = skin_manager.AC_PATH
        self.create_widgets()

    def set_skin_display_frame(self, skin_display_frame) -> None:
        self.skin_display_frame = skin_display_frame

    def create_widgets(self) -> None:
        # Car selection
        select_car_frame = ttk.LabelFrame(self, text="Select Car")
        select_car_frame.pack(padx=10, pady=10, fill="x")

        self.car_combobox = ttk.Combobox(
            select_car_frame, values=self.skin_manager.cars
        )
        self.car_combobox.pack(padx=10, pady=10)
        self.car_combobox.bind("<<ComboboxSelected>>", self.update_selection)
        if self.skin_manager.cars:
            self.car_combobox.current(0)

        # ROR names buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        add_ror_names_button = ttk.Button(
            button_frame, text="Add ROR Names", command=self.add_ror_names
        )
        add_ror_names_button.pack(side="left", padx=10)
        remove_ror_names_button = ttk.Button(
            button_frame, text="Remove ROR Names", command=self.remove_ror_names
        )
        remove_ror_names_button.pack(side="left", padx=10)

    def update_selection(self, _) -> None:
        self.skin_manager.update_car_data(self.car_combobox.get())
        self.skin_display_frame.render_renames()

    # should move this function to backend
    def add_ror_names(self) -> None:
        ror_html = sd.askstring("Input", "Paste ROR skin names HTML here:")
        if not ror_html:
            return

        parser = RorHTMLParser()
        parser.feed(ror_html)
        self.skin_manager.ror_names = parser.ror_skins

        if (
            save_ror_names(
                self.AC_PATH, self.car_combobox.get(), self.skin_manager.ror_names
            )
            == -1
        ):
            print("Error saving ror names")

        self.update_selection(None)

    # should move this function to backend
    def remove_ror_names(self) -> None:
        self.skin_manager.ror_names = []
        if (
            save_ror_names(
                self.AC_PATH, self.car_combobox.get(), self.skin_manager.ror_names
            )
            == -1
        ):
            print("Error removing ror names")

        self.update_selection(None)
