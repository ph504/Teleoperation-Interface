import csv


class Logger():
    
    fields = ["Event", "Value", "Timestamp"]
    
    def __init__(self) -> None:
        pass

    def log(event, value, time_stamp):
        with open('profiles3.csv', 'w', newline='') as file: 
            writer = csv.DictWriter(file, fieldnames = Logger.fields, dialect='excel')
            writer.writeheader() 








if __name__ == "__main__":
    Logger.log("event","value","timestamp")