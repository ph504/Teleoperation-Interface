from tkinter import Label
from PIL import Image, ImageTk

javatar_info = {
    "x": 510,
    "y": 800,
    "width": 150,
    "height": 180,
}


javatar_images = {
    "default" : "/home/pouya/catkin_ws/src/test/src/images/cartoon-jackal-006.png",
    "happy" : "/home/pouya/catkin_ws/src/test/src/images/linkedin.png",
    "sad" : "sdfsgfbgegefgfd"

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

    def change_image(self,state):
        self.image = Image.open(javatar_images[state]).resize((self.width,self.height), Image.ANTIALIAS)
        self.imagetk = ImageTk.PhotoImage(self.image)
        self.label.config(image = self.imagetk)
        self.label.image = self.imagetk