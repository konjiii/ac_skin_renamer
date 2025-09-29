# the forlder F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins
import os
import pickle
from pathlib import Path
class alexrename():
    def __init__(self, drivers, rorzone_skin_names, skin_dict ,save_file="test_save_file", skinpath = Path(""), savefile_location = Path("")):
        self.drivers=drivers                       # original drivers and rorzone skinnames
        self.rorzone_skin_names=rorzone_skin_names # init dict that keeps track of driver and rorzone skin name combo
        self.skin_dict = skin_dict 
        self.save_file = save_file                 # init savefile (to save skin_dict)
        if savefile_location == Path(""):
            self.savefile_location = Path.cwd()/save_file
        if skinpath == Path(""):
            self.skinpath = Path.cwd()/"skins"

    @staticmethod
    def rename_path(old_dir, new_dir):
        """Rename folder, old becomes new."""
        old_dir.rename(new_dir)
        print(f"Renamed folder:\n{old_dir}\n→ {new_dir}") #hier mag weg
    @staticmethod
    def get_folders(folderpath=Path.cwd()):
        """Get all folders in dir. No input: dir is the dir of this file."""
        folders = [f.name for f in folderpath.iterdir() if f.is_dir()]
        return folders

    # save and load
    @staticmethod
    def save(var,filename="testfile"):
        with open(filename, "wb") as file: 
            pickle.dump(var, file)
    @staticmethod
    def load(filename="testfile"):
        with open(filename, "rb") as file: 
            return pickle.load(file)

    def set_back_to_original(self):
        for driver in drivers:
            self.change_skin(chosen_driver=driver, chosen_rorzone=driver)

    def change_skin(self, chosen_driver, chosen_rorzone):
            if (self.savefile_location).exists(): # check for save file
                self.skin_dict = self.load(save_file) # get remembered configuration
                
            skin_current = self.get_folders(self.skinpath) # get current folder names
            if set(list(self.skin_dict.values()))!=set(skin_current): # current folder names are not the skin names (doesnt correspond)
                print(self.skin_dict.values())
                print(skin_current)
                print(f"Current files in dir are not corresponding skin names. We are in dir: {self.skinpath}")
                return
            
            # RENAME THE FOLDER
            old_skin = skin_dict[chosen_driver]
            new_skin = chosen_rorzone
            self.rename_path(old_dir=self.skinpath/old_skin, new_dir=self.skinpath/new_skin)
            # update skin dict
            skin_dict[chosen_driver] = chosen_rorzone
            self.save(skin_dict, save_file)

    def show_drivers(self):
        for k, v in enumerate(self.drivers):
            print(f"{k}: {v}")

    def show_rorzone(self):
        for i, elem in enumerate(self.rorzone_skin_names):
            print(f"{i}: {elem}")
        
if __name__ == "__main__":
    # init
    drivers=['A525_10_Gasly', 'AMR25_18_Stroll', 'APXGP_7_Hayes_Miami', 'APXGP_9_Pearce_Miami', 'C45_27_Hulkenberg', 'C45_5_Bortoleto', 'FW47_23_Albon', 'FW47_55_Sainz', 'MCL39_4_Norris', 'MCL39_81_Piastri', 'RB21_1_Verstappen', 'RB21_22_Tsunoda', 'RB21_30_Lawson', 'RB21_Japan_1_Verstappen', 'RB21_Japan_22_Tsunoda', 'SF23_Test_Hamilton', 'SF25_16_Leclerc', 'SF25_44_Hamilton', 'SF25_Miami_16_Leclerc', 'SF25_Miami_44_Hamilton', 'VCARB02_22_Tsunoda', 'VCARB02_30_Lawson', 'VCARB02_6_Hadjar', 'VCARB02_Miami_30_Lawson', 'VCARB02_Miami_6_Hadjar', 'VF25_31_Ocon', 'VF25_87_Bearman', 'W16_12_Antonelli', 'W16_63_Russell', 'A525_7_Doohan', 'AMR25_14_Alonso']
    rorzone_skin_names=['benwood_racing_14', 'benwood_racing_15', 'detroit_motorsports_04', 'detroit_motorsports_34', 'enstone_racing_42', 'enstone_racing_61', 'fortix_vrc_racing_08', 'fortix_vrc_racing_96', 'milloms_fa_18', 'milloms_fa_24', 'panther_racing_05', 'panther_racing_06', 'revision_racing_17', 'revision_racing_45', 'vrc_motorsport_07', 'vrc_motorsport_29']
    # init dict that keeps track of driver and rorzone skin name combo
    skin_dict = {elem: elem for elem in drivers}
    # init savefile (to save skin_dict)
    save_file = "skinfile"
    bone= alexrename(drivers=drivers, rorzone_skin_names=rorzone_skin_names,skin_dict=skin_dict,save_file=save_file)

    for i in range(1):
        # example for checking if safe file exists.
        if (Path.cwd()/save_file).exists():
            skin_dict = bone.load(save_file)
            print("yup")
        
        # if you want to get the original back, answer yes
        if input("Set skins back to original?:[y/n]").lower().startswith("y"):
            bone.set_back_to_original()

        else:
            bone.show_drivers()
            driver_int = int(input("choose driver:"))
            chosen_driver = drivers[driver_int]
            print("-----------------------\n\n\n\n")
            bone.show_rorzone()
            ror_int = int(input("choose rorzone:"))
            chosen_rorzone = rorzone_skin_names[ror_int]
            # skinpath = rf"F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins"
            bone.change_skin(chosen_driver,chosen_rorzone)
    

