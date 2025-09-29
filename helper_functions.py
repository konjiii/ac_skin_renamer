import pickle

def valid_path(path):
    import os
    return path is not None and os.path.exists(path) and os.path.isdir(path)


def get_settings():
    with open("settings.pkl", "rb") as f:
        return pickle.load(f)