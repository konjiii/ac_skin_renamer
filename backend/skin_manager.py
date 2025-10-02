from pathlib import Path
from backend.file_io_functions import get_cars, get_ror_names, get_skins, get_renames


class SkinManager:
    """
    Handles backend logic
    """
    def __init__(self, AC_PATH):
        self.AC_PATH = AC_PATH

        self.cars = get_cars(self.AC_PATH)
        self.skins = []
        self.ror_names = []

        self.renames = get_renames(self.AC_PATH, self.cars[0]) if self.cars else {}
        print(self.renames)

    def update_car_data(self, selected_car) -> None:
        """Update skins and ror_names based on the selected car and re-render."""
        if not selected_car:
            return
            
        self.skins = get_skins(self.AC_PATH, selected_car)
        self.ror_names = get_ror_names(self.AC_PATH, selected_car)
        self.renames = get_renames(self.AC_PATH, selected_car)
        print(f"Updated car data for {selected_car}:\nSkins: {self.skins}\nROR Names: {self.ror_names}\nRenames: {self.renames}")

    @staticmethod
    def rename_path(old_dir, new_dir):
        """Rename folder, old becomes new."""
        old_dir.rename(new_dir)
        print(f"Renamed folder:\n{old_dir}\n→ {new_dir}")