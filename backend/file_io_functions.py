import os
import json
from typing import Any
from pathlib import Path
import globals


def save(var: Any, path: Path) -> None:
    """
    Save variable to a pickle file.

    :param var: variable to save
    :param path: path to the pickle file
    :return: None
    """
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as file:
        json.dump(var, file)


def load(path: Path) -> Any:
    """
    Load variable from a json file.

    :param path: path to the json file
    :return: variable loaded from the json file
    """
    with open(path, "r") as file:
        return json.load(file)


def get_cars(ac_path: Path) -> list[str]:
    """
    Find all cars in the cars directory of AC installation

    :param ac_path: path to AC installation
    :return: list of cars (folder names)
    """
    cars_folder = ac_path / "content" / "cars"
    if not cars_folder.exists():
        return []
    return [dir.name for dir in cars_folder.iterdir() if dir.is_dir()]


def get_skins(ac_path: Path, save_path: Path, car_name: str) -> list[str]:
    """
    Find skin_list.json in skin directory of selected car. If not found, create it with current skins in directory.

    :param ac_path: path to AC installation
    :param save_path: path to save directory
    :param car_name: name of the car (folder name)
    :return: list of skins (folder names)
    """
    skins_folder = ac_path / "content" / "cars" / car_name / "skins"
    skins_file = save_path / car_name / "skin_list.json"

    if not skins_folder.exists():
        return []

    if skins_file.exists():
        return load(skins_file)

    skins = [dir.name for dir in skins_folder.iterdir() if dir.is_dir()]

    save(skins, skins_file)

    return skins


def get_ror_names(save_path: Path, car_name: str) -> list[str]:
    """
    Find ror_names in the skin directory of the selected car.

    :param ac_path: path to AC installation
    :param car_name: name of the car (folder name)
    :return: list of ror_names (folder names)
    """
    ror_file = save_path / car_name / "ror_list.json"

    if not ror_file.exists():
        return []

    return load(ror_file)


def save_ror_names(save_path: Path, car_name: str, ror_names: list[str]) -> int:
    """
    Save list of ror_names in the skin directory of the selected car.

    :param ac_path: path to AC installation
    :param car_name: name of the car (folder name)
    :param ror_names: list of ror_names to save
    :return: int: -1 if error, 0 if success
    """
    ror_file = save_path / car_name / "ror_list.json"

    save(ror_names, ror_file)

    return 0


def get_settings() -> dict[str, str]:
    """
    Load settings from a json file.

    :return: dict: settings dictionary
    """
    return load(globals.ROOT_DIR / "settings.json")


def valid_path(path: str | None) -> bool:
    """
    Check if the provided path is a valid directory.

    :param path: path to check
    :return: bool: True if valid, False otherwise
    """
    return path is not None and os.path.exists(path) and os.path.isdir(path)


def save_ac_path(settings: dict) -> None:
    """
    Save the Assetto Corsa path to settings.json.

    :param settings: settings dictionary
    """
    save(settings, globals.ROOT_DIR / "settings.json")


def get_renames(save_path: Path, car_name: str) -> dict:
    """
    Get the rename dictionary file contents.

    :param ac_path: path to AC installation
    :param car_name: name of the car (folder name)
    :return: str: rename dictionary
    """
    renames_file = save_path / car_name / "rename_dict.json"

    if not renames_file.exists():
        renames_dict = {}
        save(renames_dict, renames_file)
        return renames_dict

    return load(renames_file)


def save_renames(save_path: Path, car_name: str, renames: dict) -> int:
    """
    Save the rename dictionary file contents.

    :param ac_path: path to AC installation
    :param car_name: name of the car (folder name)
    :param renames: rename dictionary to save
    :return: int: -1 if error, 0 if success
    """
    renames_file = save_path / car_name / "rename_dict.json"

    save(renames, renames_file)

    return 0
