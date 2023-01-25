from tkinter import *
import time
import PIL.Image
from PIL import ImageTk
import threading

flashing_image_info = {
    "x": 1600,
    "y": 800,
    "width": 200,
    "height": 180,
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

