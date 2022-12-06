import time
import tkinter
from PIL import Image, ImageTk
import math

top = tkinter.Tk()

C = tkinter.Canvas(top, bg="white", height=500, width=500)

angle_in_degrees = 0

angle_in_radians = angle_in_degrees * math.pi / 180
line_length = 100
center_x = 250
center_y = 250
end_x = center_x + line_length * math.cos(angle_in_radians)
end_y = center_y + line_length * math.sin(angle_in_radians)



line = C.create_line(center_x, center_y, end_x, end_y)



top.bind('r', lambda e: rotate())


def rotate():
    global angle_in_degrees
    global line 
    angle_in_degrees += 5
    print("hey")
    angle_in_radians = angle_in_degrees * math.pi / 180
    line_length = 100
    center_x = 250
    center_y = 250
    end_x = center_x + line_length * math.cos(angle_in_radians)
    end_y = center_y + line_length * math.sin(angle_in_radians)
    C.delete('all')
    line = C.create_line(center_x, center_y, end_x, end_y)




C.pack()
top.mainloop()