import os
import pickle
from typing import Any

def save(var: Any, path: str) -> None:
    """
    Save variable to a pickle file.

    parameters:
        var: variable to save
        path: path to the pickle file
    returns:
        None
    """
    with open(path, "wb") as file: 
        pickle.dump(var, file)

def load(path: str) -> Any:
    """
    Load variable from a pickle file.
    parameters:
        path: path to the pickle file
    returns:
        variable loaded from the pickle file
    """
    with open(path, "rb") as file: 
        return pickle.load(file)

def get_cars(ac_path: str) -> list[str]:
    """
    Find all cars in the cars directory of AC installation

    parameters:
        ac_path: path to AC installation
    returns:
        list of cars (folder names)
    """
    cars_folder = os.path.join(ac_path, "content", "cars")
    if not os.path.exists(cars_folder):
        return []
    return os.listdir(cars_folder)

def get_skins(ac_path: str, car_name: str) -> list[str]:
    """
    Find skin_list.pkl in skin directory of selected car. If not found, create it with current skins in directory.

    parameters:
        ac_path: path to AC installation
        car_name: name of the car (folder name)
    returns:
        list of skins (folder names)
    """
    skins_folder = os.path.join(ac_path, "content", "cars", car_name, "skins")
    skins_file = os.path.join(skins_folder, "skin_list.pkl")

    if not os.path.exists(skins_folder):
        return []

    if os.path.exists(skins_file):
        return load(skins_file)

    skins = os.listdir(skins_folder)

    save(skins, skins_file)

    return skins

def get_ror_names(ac_path: str, car_name: str) -> list[str]:
    """
    Find ror_names in the skin directory of the selected car.

    parameters:
        ac_path: path to AC installation
        car_name: name of the car (folder name)
    returns:
        list of ror_names (folder names)
    """
    skins_folder = os.path.join(ac_path, "content", "cars", car_name, "skins")
    ror_file = os.path.join(skins_folder, "ror_list.pkl")
    if not os.path.exists(skins_folder):
        return []

    if not os.path.exists(ror_file):
        return []

    return load(ror_file)

def save_ror_names(ac_path: str, car_name: str, ror_names: list[str]) -> int:
    """
    Save list of ror_names in the skin directory of the selected car.

    parameters:
        ac_path: path to AC installation
        car_name: name of the car (folder name)
        ror_names: list of ror_names to save
    returns:
        int: -1 if error, 0 if success
    """
    skins_folder = os.path.join(ac_path, "content", "cars", car_name, "skins")
    ror_file = os.path.join(skins_folder, "ror_list.pkl")
    if not os.path.exists(skins_folder):
        return -1

    save(ror_names, ror_file)

    return 0

def get_settings() -> dict:
    """
    Load settings from a pickle file.
    
    returns:
        dict: settings dictionary
    """
    return load("settings.pkl")

def valid_path(path: str) -> bool:
    """
    Check if the provided path is a valid directory.
    
    parameters:
        path: path to check
    returns:
        bool: True if valid, False otherwise
    """
    import os
    return path is not None and os.path.exists(path) and os.path.isdir(path)

def save_ac_path(settings: dict) -> int:
    """
    Save the Assetto Corsa path to settings.pkl.
    
    parameters:
        settings: settings dictionary
    returns:
        int: -1 if error, 0 if success
    """
    return save(settings, "settings.pkl")

def get_renames(ac_path: str, car_name: str) -> dict:
    """
    Get the rename dictionary file name.

    parameters:
        ac_path: path to AC installation
        car_name: name of the car (folder name)
    returns:
        str: rename dictionary file name
    """
    skins_folder = os.path.join(ac_path, "content", "cars", car_name, "skins")
    renames_file = os.path.join(skins_folder, "rename_dict.pkl")
    if not os.path.exists(skins_folder):
        return {}

    if not os.path.exists(renames_file):
        renames_dict = {}
        save(renames_dict, renames_file)
        return renames_dict

    return load(renames_file)

def save_renames(ac_path: str, car_name: str, renames: dict) -> int:
    """
    Save the rename dictionary file name.

    parameters:
        ac_path: path to AC installation
        car_name: name of the car (folder name)
        renames: rename dictionary to save
    returns:
        int: -1 if error, 0 if success
    """
    skins_folder = os.path.join(ac_path, "content", "cars", car_name, "skins")
    renames_file = os.path.join(skins_folder, "rename_dict.pkl")
    if not os.path.exists(skins_folder):
        return -1

    save(renames, renames_file)

    return 0