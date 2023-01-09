from tkinter import *
from canvas import *

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
    def __init__(self, root):
        
        self.description_lbl = Label(root, text= "Enter the string written on each paper")
        self.description_lbl.place(x= 760, y= 340, width= 500,height= 20)

        self.entry_lbl =  Entry(root)
        self.entry_lbl.place(x= 760 ,y= 370 ,width= 500, height= 15)

        self.task_canvas = TaskCanvas(root, task_inspect_info)
        self.task_text_lbl = Label(root, text = "Dead Bodies Found:" )
        self.task_text_lbl.place(x= 900, y = 315, width = 150, height = 15)


        self.error_lbl = Label(root, text= "")
        self.error_lbl.place(x= 760, y = 400, width = 500, height = 15)
        
        self.btn_validate = Button(root, text= "Validate" , command= self.validate)
        self.btn_validate.place(x = 885, y = 430, width = 250, height = 25)

        self.task_count = 0

        self.code_list = [
                            "pKFRjK8wr8",
                            "bRaVW4Wd9M",
                            "OjXocXGnMI",
                            "klNxjOeSGD",
                            "A2QYx8g23O",
                            "td9jRJtRGH",
                            "ONCHwPQZNh",
                            "KATT4jRex9",
                            "oMSe5089Zs",
                            "bA2R7nkV8q"
                            ]
        self.code_list_used = []
        


    
    
    
    def validate(self):
            string = str(self.entry_lbl.get())
            self.entry_lbl.delete(0, len(string))
     
            if string in self.code_list_used:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg="green", text="This has been validated before!")

        
            elif string in self.code_list:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "green", text="you got a new dead body!")
                self.code_list.remove(string)
                self.code_list_used.append(string)
                self.task_count += 1
                self.task_canvas.plus_inspect()
            
            elif string not in self.code_list:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "red", text="The string you entered is not valid!")
            if len(self.code_list) == 0:
                self.error_lbl.configure(font=('Helvetica', '12', 'bold'), fg = "green", text="Congrats! You've checked all the dead bodies!")


            print("Task Count:" + " " + str(self.task_count))