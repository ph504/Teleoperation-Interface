import csv
from event import EventManager
import time
import global_variables

class Logger():
    
    fields = ["Event", "Value", "Timestamp"]
    dict_list = []
    elapsed_time = ""
    
    def generate_filename():
        file_name = "/home/pouya/catkin_ws/log_data/"
        file_name += str(global_variables.participant)
        if global_variables.second_round:
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
        
    def time_update(text):
        Logger.elapsed_time = text

    def write_data():
        if global_variables.tutorial_mode: return
        with open(Logger.generate_filename(), 'w', newline='') as file: 
            writer = csv.DictWriter(file, fieldnames = Logger.fields, dialect='excel')
            writer.writeheader() 
            writer.writerows(Logger.dict_list)


    EventManager.subscribe("countdown", time_update)


    
    
    