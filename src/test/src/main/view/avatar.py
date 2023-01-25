from tkinter import Label
from PIL import Image, ImageTk
import time
import threading
import event
javatar_info = {
    "x": 460,
    "y": 800,
    "width": 200,
    "height": 180,
}


javatar_images = {
    "default" : "/home/pouya/catkin_ws/src/test/src/images/default.png",
    "happy" : "/home/pouya/catkin_ws/src/test/src/images/happy.png",
    "sad" : "/home/pouya/catkin_ws/src/test/src/images/sad.png",
    "angry": "/home/pouya/catkin_ws/src/test/src/images/angry.png",
    "nonsocial": "/home/pouya/catkin_ws/src/test/src/images/jackal_nonsocial.jpg"

}


class Avatar():
    
    def __init__(self,root , avatar_info, avatar_images):
            self.x = avatar_info["x"]
            self.y = avatar_info["y"]
            self.width = avatar_info["width"]
            self.height = avatar_info["height"]
            self.image = Image.open(avatar_images["default"]).resize((self.width,self.height), Image.ANTIALIAS)
            self.imagetk = ImageTk.PhotoImage(self.image)
            self.label = Label(root)
            self.label.config(image = self.imagetk)
            self.label.image = self.imagetk
            self.label.place(x = self.x ,y = self.y ,width = self.width ,height = self.height)
            self.state = "default"

            event.subscribe("mistake", self.change_image_hit)

    def change_image(self,state):
        self.image = Image.open(javatar_images[state]).resize((self.width,self.height), Image.ANTIALIAS)
        self.state = state
        self.imagetk = ImageTk.PhotoImage(self.image)
        self.label.config(image = self.imagetk)
        self.label.image = self.imagetk

    def change_image_temp(self,state):
        def swap_images(s, p_s):
            self.change_image(s)
            time.sleep(10)
            self.change_image(p_s)
        prev_state = self.state
        t = threading.Thread(target=swap_images, args=(state, prev_state))
        t.start()

    def change_image_hit(self, dummy):
        def swap_images(s, p_s):
            self.change_image(s)
            time.sleep(4)
            self.change_image(p_s)
        prev_state = self.state
        t = threading.Thread(target=swap_images, args=("angry", prev_state))
        t.start()
        
      

        
        
