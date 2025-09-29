import os
import pickle

def get_cars(ac_path):
    """
    Find all cars in the cars directory of AC installation

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