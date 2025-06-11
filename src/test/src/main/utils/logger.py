from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

import csv
from main.control import event_manager
import time
from main.data import global_config as gv

class Logger():
    
    fields = ["Event", "Value", "Timestamp"]
    dict_list = []
    elapsed_time = ""
    
    @staticmethod
    def generate_filename():
        file_name = "/home/ph504/Desktop/Projects/Teleoperation-Interface"
        file_name += str(gv.participant)
        if gv.second_round:
            file_name += "_2"
        else:
            file_name += "_1"
        
        file_name += ".csv"
        print(f"***ARYA DEBUG LOG :: filename is {file_name}")
        return file_name
        

    @staticmethod
    def log(event, value):    
        Logger.dict_list.append({"Event": event, "Value": value, "Timestamp": Logger.elapsed_time})
        Logger.write_data()
    

    @staticmethod
    def write_data():
        if gv.tutorial_mode: return
        with open(Logger.generate_filename(), 'w', newline='') as file: 
            writer = csv.DictWriter(file, fieldnames = Logger.fields, dialect='excel')
            writer.writeheader() 
            writer.writerows(Logger.dict_list)


    # def __init__(self) -> None:
    #     pass
    
    
    