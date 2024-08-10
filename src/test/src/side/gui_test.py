
from tkinter import *
from tkinter import ttk
from tkinter.tix import IMAGE
from PIL import ImageTk, Image


root = Tk()

root.geometry("1920x1080")
root.title("hello")

pinterestframe= Frame(root)
linkedinframe = Frame(root)

pinterestframe.grid(column=0, row=0)
linkedinframe.grid(column=0, row=1)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

image1 = ImageTk.PhotoImage(Image.open("/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/pinterest.png").resize((400,300), Image.ANTIALIAS))
image2 = ImageTk.PhotoImage(Image.open("/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/linkedin.png").resize((800,600), Image.ANTIALIAS))

lbl1= Label(pinterestframe)
lbl1.config(image = image1)
lbl1.image = image1

lbl2 = Label(linkedinframe, image=image2).grid(column=0,row=0)


root.mainloop()