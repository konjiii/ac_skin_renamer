import os
import pickle

def get_cars(ac_path):
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

def get_skins(ac_path, car_name):
    """
    Find skin_list.pkl in skin directory of selected car. If not found, create it with current skins in directory.

    parameters:
        ac_path: path to AC installation
        car_name: name of the car (folder name)
    returns:
        list of skins (folder names)
    """
    skins_folder = os.path.join(ac_path, "content", "cars", car_name, "skins")

    if not os.path.exists(skins_folder):
        return []

    if os.path.exists(os.path.join(skins_folder, "skin_list.pkl")):
        with open(os.path.join(skins_folder, "skin_list.pkl"), "rb") as f:
            return pickle.load(f)
    
    skins = os.listdir(skins_folder)
    skin_list_path = os.path.join(skins_folder, "skin_list.pkl")

    with open(skin_list_path, "wb") as f:
        pickle.dump(skins, f)

    return skins

def get_ror_names(ac_path, car_name):
    """
    Find ror_names in the skin directory of the selected car.

    parameters:
        ac_path: path to AC installation
        car_name: name of the car (folder name)
    returns:
        list of ror_names (folder names)
    """
    skins_folder = os.path.join(ac_path, "content", "cars", car_name, "skins")
    if not os.path.exists(skins_folder):
        return []
    
    if not os.path.exists(os.path.join(skins_folder, "ror_list.pkl")):
        return []

    with open(os.path.join(skins_folder, "ror_list.pkl"), "rb") as f:
        return pickle.load(f)
    
def save_ror_names(ac_path, car_name, ror_names) -> int:
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
    if not os.path.exists(skins_folder):
        return -1
    
    with open(os.path.join(skins_folder, "ror_list.pkl"), "wb") as f:
        pickle.dump(ror_names, f)

    return 0

def get_settings() -> dict:
    """
    Load settings from a pickle file.
    
    returns:
        dict: settings dictionary
    """
    with open("settings.pkl", "rb") as f:
        return pickle.load(f)
    
def valid_path(path) -> bool:
    """
    Check if the provided path is a valid directory.
    
    parameters:
        path: path to check
    returns:
        bool: True if valid, False otherwise
    """
    import os
    return path is not None and os.path.exists(path) and os.path.isdir(path)

def save_ac_path(settings) -> int:
    """
    Save the Assetto Corsa path to settings.pkl.
    
    parameters:
        settings: settings dictionary
    returns:
        int: -1 if error, 0 if success
    """
    try:
        with open("settings.pkl", "wb") as f:
            pickle.dump(settings, f)
    except Exception as e:
        print(f"Error saving AC path: {e}")
        return -1
    return 0