from pathlib import Path
from backend.file_io_functions import (
    get_cars,
    get_ror_names,
    get_skins,
    get_renames,
    save_renames,
)
import pyperclip
import json


class SkinManager:
    """
    Handles backend logic
    """

    def __init__(self, AC_PATH):
        self.AC_PATH = AC_PATH

        self.cars = get_cars(self.AC_PATH)

        self.selected_car = None
        self.skins = []
        self.ror_names = []

        self.rename_comboboxes = {}
        self.renames = get_renames(self.AC_PATH, self.cars[0]) if self.cars else {}
        self.to_rename = {}

    def update_car_data(self, selected_car: str) -> None:
        """Update skins and ror_names based on the selected car and re-render."""
        if not selected_car:
            return

        self.skins = get_skins(self.AC_PATH, selected_car)
        self.ror_names = get_ror_names(self.AC_PATH, selected_car)
        self.renames = get_renames(self.AC_PATH, selected_car)
        self.selected_car = selected_car
        self.to_rename.clear()
        self.rename_comboboxes.clear()
        print(
            f"Updated car data for {selected_car}:\nSkins: {self.skins}\nROR Names: {self.ror_names}\nRenames: {self.renames}"
        )

    @staticmethod
    def rename_path(old_dir, new_dir):
        """Rename folder, old becomes new."""
        old_dir.rename(new_dir)
        print(f"Renamed folder:\n{old_dir}\n→ {new_dir}")

    def update_skin_mapping(self, ror_name: str, skin_name: str) -> None:
        """Update the mapping of a skin name to a ROR name."""
        if ror_name in self.ror_names and skin_name in self.skins:
            if skin_name in self.to_rename.values():
                # Remove any existing mapping with this skin_name
                existing_ror = next(
                    (k for k, v in self.to_rename.items() if v == skin_name), None
                )
                if existing_ror:
                    del self.to_rename[existing_ror]
                    self.rename_comboboxes[existing_ror].set(
                        ""
                    )  # Clear the combobox selection
                    print(f"Removed existing mapping: {skin_name} → {existing_ror}")
            self.to_rename[ror_name] = skin_name
            print(f"Updated mapping: {skin_name} → {ror_name}")
        else:
            print(f"Invalid ROR name or skin name: {skin_name}, {ror_name}")

        print(self.to_rename)

    def apply_changes(self) -> None:
        """Apply the renaming changes."""
        if not self.to_rename:
            print("No changes to apply.")
            return

        if not self.selected_car:
            print("No valid car selected.")
            return

        skins_folder = (
            Path(self.AC_PATH) / "content" / "cars" / self.selected_car / "skins"
        )

        failed = False
        for ror_name, skin_name in self.to_rename.items():
            old_dir = skins_folder / skin_name
            new_dir = skins_folder / ror_name
            if not old_dir.exists():
                failed = True
                print(f"Cannot rename {old_dir} → {new_dir}: source does not exist.")
            elif new_dir.exists():
                failed = True
                print(f"Cannot rename {old_dir} → {new_dir}: target already exists.")
            else:
                self.rename_path(old_dir, new_dir)
                self.renames[ror_name] = skin_name

        save_renames(self.AC_PATH, self.selected_car, self.renames)

        self.to_rename.clear()
        if failed:
            print("Some changes could not be applied due to errors.")
            return
        print("All changes applied.")

    def reset_changes(self) -> None:
        """Reset all renaming changes."""
        if not self.selected_car:
            print("No valid car selected.")
            return

        self.to_rename.clear()

        failed = False
        to_remove = list()
        for ror_name, skin_name in self.renames.items():
            # fmt: off
            old_dir = Path(self.AC_PATH) / "content" / "cars" / self.selected_car / "skins" / ror_name
            new_dir = Path(self.AC_PATH) / "content" / "cars" / self.selected_car / "skins" / skin_name
            # fmt: on

            if not old_dir.exists():
                failed = True
                print(f"Cannot rename {old_dir} → {new_dir}: source does not exist.")
            elif new_dir.exists():
                failed = True
                print(f"Cannot rename {old_dir} → {new_dir}: target already exists.")
            else:
                self.rename_path(old_dir=old_dir, new_dir=new_dir)
                to_remove.append(ror_name)

        for ror_name in to_remove:
            del self.renames[ror_name]

        save_renames(self.AC_PATH, self.selected_car, self.renames)

        for ror_name, combobox in self.rename_comboboxes.items():
            combobox.set("")  # Clear the combobox selection

        if failed:
            print("Some changes could not be reset due to errors.")
            return
        print("All changes have been reset.")

    def copy_configuration(self) -> int:
        """
        Copy current renames to clipboard.
        
        Returns:
            0 on success, -1 if there are no renames to copy.
        """
        if self.renames == {}:
            print("No renames to copy.")
            return -1

        pyperclip.copy(json.dumps(self.renames))
        print("Copied current configuration to clipboard.")
        return 0

    def paste_configuration(self, config_text: str) -> None:
        """Paste renames from clipboard."""
        # try to parse clipboard content
        try:
            config_parsed = json.loads(config_text)
        except ValueError:
            print("HE IS TRYING TO HACK YOU! DONT LISTEN TO HI>$!**(*)")
            return
        if type(config_parsed) is not dict:
            raise TypeError("Not a dict after eval")

        # check if provided config is valid for current car
        for ror, skin in config_parsed.items():
            if ror not in self.ror_names or skin not in self.skins:
                print(f"Invalid ROR name or skin name in pasted config: {skin}, {ror}")
                return

        # first reset to original state
        self.reset_changes()
        print("pasting configuration")
        # then apply new config
        self.to_rename = config_parsed
        self.apply_changes()
