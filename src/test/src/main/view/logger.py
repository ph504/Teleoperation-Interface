import csv
from event import EventManager
import time


class Logger():
    
    fields = ["Event", "Value", "Timestamp"]
    dict_list = []
    elapsed_time = ""
  
        
    def __init__(self) -> None:
        pass

    def log(event, value):    
        Logger.dict_list.append({"Event": event, "Value": value, "Timestamp": Logger.elapsed_time})
        Logger.write_data()
        
    def time_update(text):
        Logger.elapsed_time = text

    def write_data():
        with open('p0.csv', 'w', newline='') as file: 
            writer = csv.DictWriter(file, fieldnames = Logger.fields, dialect='excel')
            writer.writeheader() 
            writer.writerows(Logger.dict_list)


    EventManager.subscribe("countdown", time_update)


    
    
    