# the forlder F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins
import os
import pickle
from pathlib import Path

def rename_path(old_dir, new_dir):
    # old_dir = Path(r"C:\Users\Nooit\OneDrive\Documenten\code voor de lol\macro's\wowmapje2")
    # new_dir = Path(r"C:\Users\Nooit\OneDrive\Documenten\code voor de lol\macro's\wowmapje")

    old_dir.rename(new_dir)

    print(f"Renamed folder:\n{old_dir}\n→ {new_dir}")

# os.symlink(r"orineel_pad","linknaam")

def get_folders(folderpath=Path.cwd()):
    # folder_path = Path(r"C:\Users\Nooit\OneDrive\Documenten\code voor de lol\macro's")
    # folder_path = Path(r"F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins")
    folders = [f.name for f in folderpath.iterdir() if f.is_dir()]
    return folders
# folder_path = Path(r"F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins")
# print(get_folders(folder_path))

# save and load
def save(var,filename="testfile"):
    with open(filename, "wb") as file: 
        pickle.dump(var, file)

def load(filename="testfile"):
    with open(filename, "rb") as file: 
        return pickle.load(file)

# save(folders, "testfiles")
# a=load("testfiles")
# print(a)

#original drivers and rorzone skinnames
drivers=['A525_10_Gasly', 'AMR25_18_Stroll', 'APXGP_7_Hayes_Miami', 'APXGP_9_Pearce_Miami', 'C45_27_Hulkenberg', 'C45_5_Bortoleto', 'FW47_23_Albon', 'FW47_55_Sainz', 'MCL39_4_Norris', 'MCL39_81_Piastri', 'RB21_1_Verstappen', 'RB21_22_Tsunoda', 'RB21_30_Lawson', 'RB21_Japan_1_Verstappen', 'RB21_Japan_22_Tsunoda', 'SF23_Test_Hamilton', 'SF25_16_Leclerc', 'SF25_44_Hamilton', 'SF25_Miami_16_Leclerc', 'SF25_Miami_44_Hamilton', 'VCARB02_22_Tsunoda', 'VCARB02_30_Lawson', 'VCARB02_6_Hadjar', 'VCARB02_Miami_30_Lawson', 'VCARB02_Miami_6_Hadjar', 'VF25_31_Ocon', 'VF25_87_Bearman', 'W16_12_Antonelli', 'W16_63_Russell', 'A525_7_Doohan', 'AMR25_14_Alonso']
rorzone_skin_names=['benwood_racing_14', 'benwood_racing_15', 'detroit_motorsports_04', 'detroit_motorsports_34', 'enstone_racing_42', 'enstone_racing_61', 'fortix_vrc_racing_08', 'fortix_vrc_racing_96', 'milloms_fa_18', 'milloms_fa_24', 'panther_racing_05', 'panther_racing_06', 'revision_racing_17', 'revision_racing_45', 'vrc_motorsport_07', 'vrc_motorsport_29']
# init dict that keeps track of driver and rorzone skin name combo
skin_dict = {elem: elem for elem in drivers}

def show_drivers():
    for k, v in enumerate(drivers):
        print(f"{k}: {v}")
def show_rorzone():
    for i, elem in enumerate(rorzone_skin_names):
        print(f"{i}: {elem}")

for i in range(1):
    show_drivers()
    driver_int = int(input("choose driver:"))
    chosen_driver = drivers[driver_int]
    show_rorzone()
    ror_int = int(input("choose rorzone:"))
    chosen_rorzone = rorzone_skin_names[ror_int]

    # RENAME THE FOLDER
    old_skin = skin_dict[chosen_driver]
    new_skin = chosen_rorzone
    old_dir=rf"F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins\{old_skin}"
    new_dir=rf"F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins\{new_skin}"
    rename_path(old_dir=Path(old_dir),new_dir=Path(new_dir))
    # update skin dict
    skin_dict[chosen_driver] = chosen_rorzone
    save(skin_dict, "skinfile")