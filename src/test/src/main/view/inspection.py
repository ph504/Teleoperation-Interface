from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

import tkinter as tk
from main.control import event_manager
from main.utils import logger
from main.view import canvas
import time
import threading
from main.data import global_config as gv
from main.data import global_statics as gs

class InspectionPage():
    def __init__(self, root):
        
        self.description_lbl = tk.Label(root, fg=gs.FG_COLOR, bg=gs.DARK_BG, text= "Enter the string written on each paper")
        self.description_lbl.place(x= 760, y= 340, width= 500,height= 20)

        # simple text for TODO
        self.entry_lbl =  tk.Entry(root)
        self.entry_lbl.place(x= 760 ,y= 370 ,width= 500, height= 25)

        self.error_lbl = tk.Label(root, bg=gs.DARK_BG, text= "")
        self.error_lbl.place(x= 760, y = 405, width = 500, height = 25)
        
        self.btn_validate = tk.Button(root, text= "Validate" , command= self.validate)
        self.btn_validate.place(x = 885, y = 430, width = 250, height = 25)

        # self.task_canvas = task_canvas
        # self.task_count = 0

        self.code_list = ["pKFRjK8wr8",
                          "bRaVW4Wd9M",]
        
        self.tutorial_code_list = ["DbWjNBjgfJ",
                                   "ARvttUYzBp",]
        
        self.code_list_used = []
        self.delay = False
        self.wait = False

    def clear_wait_flag(self):
         self.wait = False

    def try_again(self):
         self.wait = True

    def delete_err_lbl(self):
        def del_lbl():
                time.sleep(5)
                self.error_lbl.config(text="")
        q = threading.Thread(target= del_lbl)
        q.start()


    def deactive_forawhile(self):
         self.btn_validate.configure(state=tk.DISABLED)
         time.sleep(1)
         self.btn_validate.configure(state=tk.ACTIVE)
         
    def validate(self):
            string = str(self.entry_lbl.get())
            self.entry_lbl.delete(0, len(string))
            
            if string in self.code_list_used:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg="yellow", text="This equipment has been validated before.") # type: ignore
                logger.Logger.log("duplicated_entry", "N/A") # type: ignore
                event_manager.EventManager.post_event("duplicate_entry")
                self.delete_err_lbl()

        
            elif string in self.code_list or string in self.tutorial_code_list:
                if self.wait:
                     self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "#8c1127", text="A network error occured. Try writing it again") # type: ignore
                     self.delete_err_lbl()
                     return
                else:
                    self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "green", text="Scanned") # type: ignore
                    #playsound("/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/sounds/inspect_succ.wav", block=False)
                    gv.inspect_succ_sound.play()
                    
                    self.delete_err_lbl()
                    
                    if gv.tutorial_mode:
                        
                        self.tutorial_code_list.remove(string)
                    else:
                        self.code_list.remove(string)

                    self.code_list_used.append(string)
                    # self.task_count += 1
                    # self.task_canvas.plus()
            
            elif string not in self.code_list:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "red", text="The string you entered is not valid!") # type: ignore
                logger.Logger.log("wrong_entry", "N/A") # type: ignore
                event_manager.EventManager.post_event("wrong_entry")
                self.delete_err_lbl()
            
            if len(self.code_list) == 0:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "green", text="All the equipments have been scanned.") # type: ignore
                self.delete_err_lbl()

            x = threading.Thread(target=self.deactive_forawhile)
            x.start()

