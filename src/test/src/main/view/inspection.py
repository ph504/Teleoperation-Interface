from tkinter import *
from canvas import *
import time
import threading
import global_variables

task_inspect_info = {
    "x": 980,
    "y": 313,
    "width": 150,
    "height": 20,
    "color": "black",
    "font": ('Helvetica', '12', 'bold'),
    "active": True
}



class InspectionPage():
    def __init__(self, root, task_canvas):
        
        self.description_lbl = Label(root, text= "Enter the string written on each paper")
        self.description_lbl.place(x= 760, y= 340, width= 500,height= 20)

        self.entry_lbl =  Entry(root)
        self.entry_lbl.place(x= 760 ,y= 370 ,width= 500, height= 25)

        self.error_lbl = Label(root, text= "")
        self.error_lbl.place(x= 760, y = 405, width = 500, height = 25)
        
        self.btn_validate = Button(root, text= "Validate" , command= self.validate)
        self.btn_validate.place(x = 885, y = 430, width = 250, height = 25)

        self.task_canvas = task_canvas
        self.task_count = 0

        EventManager.subscribe("try_again", self.try_again)
        EventManager.subscribe("clear_wait_flag", self.clear_wait_flag)
        self.code_list = [
                            "pKFRjK8wr8",
                            "bRaVW4Wd9M",
                            "LLmvDKgkqk",
                            "k9NxjHeSGD", 
                            "A2QYx8g23p",
                            "MEvvKDPl2R",
                            "PB1gsUELNc",
                            "td9jRJtRGH",
                            "TNCHwPQZNh", 
                            "KATT4jRex9",
                            "5uDTPXkAn7",
                            "jMSe5a89Zs", 
                            "bA2R7nkV8q"
                            ]

        self.code_list2 = [
                            "ZIQVNKBV53", 
                            "8U92xD9MVZ",
                            "BitxAQSNSa",
                            "qnD5AmVLwN",  
                            "8HVCnhz6sj", 
                            "HzQTJ99bk4",
                            "U4fV8sZnhT", 
                            
                            ]
        
        self.tutorial_code_list = ["DbWjNBjgfJ",
                                   "ARvttUYzBp",
                                   "B4MSkAxwAh",
                                   "WeLF57Cn2F",
                                   "vTxDtdzV7b"]
        self.code_list_used = []
        
        self.delay = False

        self.wait = False


    def clear_wait_flag(self, dumy):

         self.wait = False
    def try_again(self, dummy):

         self.wait = True

    def delete_err_lbl(self):
        def del_lbl():
                time.sleep(5)
                self.error_lbl.config(text="")
        q = threading.Thread(target= del_lbl)
        q.start()


    def deactive_forawhile(self):
         self.btn_validate.configure(state=DISABLED)
         time.sleep(1)
         self.btn_validate.configure(state=ACTIVE)
         
    def validate(self):
            
            

            string = str(self.entry_lbl.get())
            self.entry_lbl.delete(0, len(string))
            
            if string in self.code_list_used:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg="yellow", text="This equipment has been validated before.")
                Logger.log("duplicated_entry", "N/A")
                EventManager.post_event("duplicate_entry")
                self.delete_err_lbl()

        
            elif string in self.code_list or string in self.code_list2 or string in self.tutorial_code_list:
                if self.wait:
                     self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "#8c1127", text="A network error occured. Try writing it again")
                     self.delete_err_lbl()
                     return
                else:
                    self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "green", text="Scanned")
                    #playsound("/home/pouya/catkin_ws/src/test/src/sounds/inspect_succ.wav", block=False)
                    global_variables.inspect_succ_sound.play()
                    
                    self.delete_err_lbl()
                    
                    if global_variables.tutorial_mode:
                        
                        self.tutorial_code_list.remove(string)
                    else:
                        self.code_list2.remove(string) if global_variables.is_code_list_2 else self.code_list.remove(string)

                    self.code_list_used.append(string)
                    self.task_count += 1
                    self.task_canvas.plus()
            
            elif string not in self.code_list or string not in  self.code_list2:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "red", text="The string you entered is not valid!")
                Logger.log("wrong_entry", "N/A")
                EventManager.post_event("wrong_entry")
                self.delete_err_lbl()
            
            if len(self.code_list) == 0 or len(self.code_list2) == 0:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "green", text="All the equipments have been scanned.")
                self.delete_err_lbl()

            x = threading.Thread(target=self.deactive_forawhile)
            x.start()

