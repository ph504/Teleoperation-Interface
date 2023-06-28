from tkinter import *
import time
import PIL.Image
from PIL import ImageTk
import threading
from canvas import BaseCanvas, RepeatedTimer
from event import EventManager
flashing_image_info = {
    "x": 1600,
    "y": 800,
    "width": 200,
    "height": 180,
}

countdown_info = {
    "x": 1215,
    "y": 941,
    "width": 25,
    "height": 25,
    "color": "black",
    "bg": '#d9d7bd',
    "font": ('Helvetica', '15', 'bold'),
    "active": FALSE

}


class FlashingImage():
    def __init__(self, root, flashing_image_info) -> None:
        self.x = flashing_image_info["x"]
        self.y = flashing_image_info["y"]
        self.width = flashing_image_info["width"]
        self.height = flashing_image_info["height"]
        self.image = PIL.Image.open("/home/pouya/catkin_ws/src/test/src/images/dangerzone.png").resize((self.width,self.height), 2)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label = Label(root)
        
        self.pause_time = 1

        self.disable()
        x = threading.Thread(target=self.flash)
        x.start()


    def flash(self):
        time.sleep(5)
        while True:
            
            time.sleep(self.pause_time)
            self.label.configure(image="")
            time.sleep(self.pause_time)
            self.label.configure(image=self.image_tk)

    def enable(self):
        self.label.place(x = self.x, y = self.y, width = self.width, height=self.height)

    def disable(self):
        self.label.place(x = 5000, y = self.y, width = self.width, height=self.height)

class CountdownCanvas(BaseCanvas):
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.seconds = '30'
        self.bg = dict_info['bg']
        self.text = self.seconds
        self.countdown = None
        self.fsm = None
        self.canvas.configure(bg = self.bg, borderwidth='1p', relief=FLAT)
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font, anchor= CENTER, justify="center")


    def start(self, dummy = 0):
        if self.countdown == None:
            self.countdown = RepeatedTimer(1, self.minus)
        else:
            self.countdown.start()
    
    def stop(self, dummy = 0):
        self.countdown.stop()
    
    def add_fsm(self, fsm):
        self.fsm = fsm

    def minus(self):
        sec = self.seconds
        sec = int(sec)

        if sec == 0:
            return
        
        sec -= 1
        
        if sec == 0 and self.fsm.is_s6:
           EventManager.post_event("freeze", -1)
           self.stop()
           

        self.seconds = str(sec) if sec >= 10 else '0' + str(sec) 
        self.text = self.seconds
    
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
 