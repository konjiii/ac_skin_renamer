from backend.file_io_functions import get_cars, get_ror_names, get_skins


class SkinManager:
    """
    Handles backend logic
    """
    def __init__(self, app):
        self.app = app

        self.cars = get_cars(self.app.AC_PATH)
        self.skins = []
        self.ror_names = []

    def update_data(self) -> None:
        """Update skins and ror_names based on the selected car and re-render."""
        selected_car = self.app.control_frame.car_combobox.get()
        if not selected_car:
            return
            
        self.skins = get_skins(self.app.AC_PATH, selected_car)
        self.ror_names = get_ror_names(self.app.AC_PATH, selected_car)