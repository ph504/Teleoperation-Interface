from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

import csv
from main.control import event_manager
# import time
import os
from main.data import global_config as gv

class Logger():
    
    fields = ["Event", "Value", "Timestamp"]
    dict_list = []
    elapsed_time = ""
    
    @staticmethod
    def generate_filename():
        file_name = "/home/ph504/Desktop/Projects/Teleoperation-Interface/log_data/"
        file_name += str(gv.participant)
        # file_name += gv.round_number
        
        file_name += ".csv"
        # print(f"***ARYA DEBUG LOG :: filename is {file_name}")
        return file_name
        
    @staticmethod
    def set_elapsed_time(time):
        # print(f"***ARYA DEBUG LOG :: Elapsed Time is {Logger.elapsed_time}")
        Logger.elapsed_time = time

    @staticmethod
    def log(event, value):    
        Logger.dict_list.append({"Event": event, "Value": value, "Timestamp": Logger.elapsed_time})
        # print(f"***ARYA DEBUG LOG :: logging happened, event {event}, value {value}, timestamp {Logger.elapsed_time}")
        Logger.write_data()
    

    @staticmethod
    def write_data():
        # if gv.tutorial_mode: return
        file_path = Logger.generate_filename()
        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as file: 
            # print(f'*** ARYA DEBUG LOG :: filename opened {Logger.generate_filename()}')
            writer = csv.DictWriter(file, fieldnames = Logger.fields, dialect='excel')
            if not file_exists or os.stat(file_path).st_size == 0:
                writer.writeheader()

            writer.writerow(Logger.dict_list[-1])


    # def __init__(self) -> None:
    #     pass
    
    
    