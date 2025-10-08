# the forlder F:\SteamLibrary\steamapps\common\assettocorsa\content\cars\vrc_formula_alpha_2024_csp\skins
import os
import pickle
from pathlib import Path
from ast import literal_eval
class alexrename():
    def __init__(self, drivers, rorzone_skin_names ,save_file="test_save_file", skinpath = Path(""), savefile_location = Path("")):
        self.drivers=drivers                               # original drivers
        self.rorzone_skin_names=rorzone_skin_names         # original rorzone skinnames
        self.skin_dict = {elem: elem for elem in drivers}  # init dict that keeps track of driver and rorzone skin name combo
        self.save_file = save_file                         # init savefile (to save self.skin_dict)
        if savefile_location == Path(""):
            self.savefile_location = Path.cwd()/save_file
        else:
            self.savefile_location = savefile_location
        if skinpath == Path(""):
            self.skinpath = Path.cwd()/"skins"
        else:
            self.skinpath = skinpath


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

    #  save and update self.skin_dict
    def dict_save(self,key,value):
        self.skin_dict[key]=value
        self.save(self.skin_dict,self.save_file)
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
                self.skin_dict = self.load(self.save_file) # get remembered configuration
                
            skin_current = self.get_folders(self.skinpath) # get current folder names
            if set(list(self.skin_dict.values()))!=set(skin_current): # current folder names are not the skin names (doesnt correspond)
                print(self.skin_dict.values())
                print(skin_current)
                print(f"Current files in dir are not corresponding skin names. We are in dir: {self.skinpath}")
                return
            
            # RENAME THE FOLDER
            old_skin = self.skin_dict[chosen_driver]
            new_skin = chosen_rorzone
            temporary_skin = new_skin+"1"
            # if the skin is already the desired name, no need to change
            if old_skin == new_skin:
                return
            # else
            if (self.skinpath/new_skin).exists(): # if map already exists, can't rename to this name
                # search where the new_skin map exists
                holding_driver = next((key for key, value in self.skin_dict.items() if value == new_skin), None)
                # rename that instance first
                self.rename_path(old_dir=self.skinpath/new_skin, new_dir=self.skinpath/temporary_skin)
                # then change old to new
                self.rename_path(old_dir=self.skinpath/old_skin, new_dir=self.skinpath/new_skin)
                # if original is available then go back to original
                if not (self.skinpath/holding_driver).exists():
                    self.rename_path(old_dir=self.skinpath/temporary_skin, new_dir=self.skinpath/holding_driver)
                    self.dict_save(holding_driver,holding_driver)
                # otherwise just make new -> old, (DONE: old is new, NOW: new is old)
                else:
                    self.rename_path(old_dir=self.skinpath/temporary_skin, new_dir=self.skinpath/old_skin)
                    self.dict_save(holding_driver,old_skin)
            else:
                self.rename_path(old_dir=self.skinpath/old_skin, new_dir=self.skinpath/new_skin)
            # update skin dict and save in pickle
            self.dict_save(chosen_driver,new_skin)

    def from_config_to_change(self, copy_skin_dict):
        if copy_skin_dict == None:
            return
        if set(copy_skin_dict.keys())!=set(self.skin_dict.keys()): # if keys not the same not correct dict!
            return
        for key in list(self.skin_dict.values()):
            driver = key
            skin_name = copy_skin_dict[key]
            self.change_skin(chosen_driver=driver, chosen_rorzone=skin_name)
            
    @staticmethod
    def get_config_from_text(copy_skin_dict_str):
        try:
            copy_skin_dict = literal_eval(copy_skin_dict_str)
        except:
            print("HE IS TRYING TO HACK YOU! DONT LISTEN TO HI>$!**(*)")
            return
        if type(copy_skin_dict) is not dict:
            raise TypeError("Not a dict after eval")
        return copy_skin_dict
    
    def show_drivers(self):
        for k, v in enumerate(self.drivers):
            print(f"{k}: {v}")
        return len(self.drivers)

    def show_rorzone(self):
        for i, elem in enumerate(self.rorzone_skin_names):
            print(f"{i}: {elem}")
        return len (self.rorzone_skin_names)
        
    

if __name__ == "__main__":
    # init
    drivers=['A525_10_Gasly', 'AMR25_18_Stroll', 'APXGP_7_Hayes_Miami', 'APXGP_9_Pearce_Miami', 'C45_27_Hulkenberg', 'C45_5_Bortoleto', 'FW47_23_Albon', 'FW47_55_Sainz', 'MCL39_4_Norris', 'MCL39_81_Piastri', 'RB21_1_Verstappen', 'RB21_22_Tsunoda', 'RB21_30_Lawson', 'RB21_Japan_1_Verstappen', 'RB21_Japan_22_Tsunoda', 'SF23_Test_Hamilton', 'SF25_16_Leclerc', 'SF25_44_Hamilton', 'SF25_Miami_16_Leclerc', 'SF25_Miami_44_Hamilton', 'VCARB02_22_Tsunoda', 'VCARB02_30_Lawson', 'VCARB02_6_Hadjar', 'VCARB02_Miami_30_Lawson', 'VCARB02_Miami_6_Hadjar', 'VF25_31_Ocon', 'VF25_87_Bearman', 'W16_12_Antonelli', 'W16_63_Russell', 'A525_7_Doohan', 'AMR25_14_Alonso']
    rorzone_skin_names=['benwood_racing_14', 'benwood_racing_15', 'detroit_motorsports_04', 'detroit_motorsports_34', 'enstone_racing_42', 'enstone_racing_61', 'fortix_vrc_racing_08', 'fortix_vrc_racing_96', 'milloms_fa_18', 'milloms_fa_24', 'panther_racing_05', 'panther_racing_06', 'revision_racing_17', 'revision_racing_45', 'vrc_motorsport_07', 'vrc_motorsport_29']
    # init savefile (to save skin_dict)
    save_file = "skinfile"
    # where to change the skins
    skinpath = Path(r"") # PUT YOUR PATH TO THE SKINS HERE!!!
    bone= alexrename(drivers=drivers, rorzone_skin_names=rorzone_skin_names,save_file=save_file,skinpath=skinpath)

    app_on=True
    while app_on:
        print("""
------------------Skin changer------------------
Options:
1: Paste configuration
2: Set skins back to original
3: Assign skins
q: quit
----------------------------------------------------""")
        # example for checking if safe file exists.
        if (Path.cwd()/bone.save_file).exists():
            bone.skin_dict = bone.load(bone.save_file)
            print("Load successful!")
        else:
            print("No load file exists or is found.")
        # Print skin_dict
        print(f"\n{bone.skin_dict}\n")
        # Selection menu:
        chosen_option=input("Choose an option: ")
        match chosen_option:
            # Paste configuration
            case "1":
                copy_skin_dict_str = input("Paste here: ")
                if copy_skin_dict_str == "q":
                    continue
                copy_skin_dict = bone.get_config_from_text(copy_skin_dict_str)
                bone.from_config_to_change(copy_skin_dict)
                print("~~~~~~~~~~~~~~Config Copied~~~~~~~~~~~~~~")
            # Set skins back to original
            case "2":
                if input("Revert to original? [y/n]").lower().startswith("y"):
                    bone.set_back_to_original()
                    print("~~~~~~~Skins set back to original~~~~~~~~")  
            # Assign skins
            case "3":
                if input("Assign skins? [y/n]").lower().startswith("y"):
                    # get driver nr
                    amount = bone.show_drivers() # get len of drivers list and print driver options
                    while True: # check input untill correct
                        driver_int = int(input("choose driver:"))
                        # if input is valid
                        if type(driver_int) is int and 0 <= driver_int and driver_int < (amount):
                            chosen_driver = drivers[driver_int] # get driver name
                            print("-----------------------\n\n\n\n")
                            break
                        else:
                            print(f"{driver_int} is not a valid option.")
                    # get rorzone nr
                    amount = bone.show_rorzone()
                    while True: # check input untill correct
                        ror_int = int(input("choose rorzone:"))
                        # if input is valid
                        if type(ror_int) is int and 0 <= ror_int and ror_int < (amount):
                            chosen_rorzone = rorzone_skin_names[ror_int] # get skin name
                            print("-----------------------\n\n\n\n")
                            bone.change_skin(chosen_driver,chosen_rorzone) # assign skin to driver
                            print("~~~~~~~~~~~~~~Skins assigned~~~~~~~~~~~~~")
                            break
                        else:
                            print(f"{ror_int} is not a valid option.")
            # Quit the app
            case "q":
                if input("Do you want to quit? [y/n]").lower().startswith("y"):
                    print("quitting program..")
                    app_on = False
            # In case of invallid options
            case _:
                print(f"The input: {chosen_option}, is not a valid command, try again!")

    print("done")