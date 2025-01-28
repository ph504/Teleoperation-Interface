import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/model/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/view/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/utils/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/test/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/data/')

import csv
import event_manager
import time
import global_config as gv

class Logger():
    
    fields = ["Event", "Value", "Timestamp"]
    dict_list = []
    elapsed_time = ""
    
    def generate_filename():
        file_name = "/home/ph504/Desktop/Projects/Teleoperation-Interface/log_data/"
        file_name += str(gv.participant)
        if gv.second_round:
            file_name += "_2"
        else:
            file_name += "_1"
        
        file_name += ".csv"
        return file_name
        
    def __init__(self) -> None:
        pass

    def log(event, value):    
        Logger.dict_list.append({"Event": event, "Value": value, "Timestamp": Logger.elapsed_time})
        Logger.write_data()
        
    @event_manager.EventManager.subscribe("countdown")
    def time_update(text):
        Logger.elapsed_time = text

    def write_data():
        if gv.tutorial_mode: return
        with open(Logger.generate_filename(), 'w', newline='') as file: 
            writer = csv.DictWriter(file, fieldnames = Logger.fields, dialect='excel')
            writer.writeheader() 
            writer.writerows(Logger.dict_list)




    
    
    