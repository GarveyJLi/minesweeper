from tkinter import *
from PIL import ImageTk, Image
import button_types
from numpy import random

#types of buttons: blank, num, and bomb, reset button
#types of button images: blank, num, bomb, flag, clicked blank, wrong flag, exploded bomb, uncovered


BUTTON_SIZE = 20

class Cell:
    def __init__(self):
        self.hidden = True
        self.hidden_text = '   '
        self.button = None
        self.to_display = self.hidden_text
        #self.button.bind("<Button-3>", right_click())
    
    def hide(self):
        self.hidden = True
        self.to_display = self.hidden_text



class NumCell(Cell):
    def __init__(self):
        super().__init__()
        self.adjacent = 0

    def reveal(self):
        self.hidden = False
        self.to_display = self.adjacent
        self.button.config(text=self.to_display)
    
    def add_adjacent(self):
        self.adjacent += 1

    def set_val(self):
        self.button.config(text=self.adjacent)

    def create_button(self, frame, xpos, ypos):
        self.button = Button(frame, text=self.to_display, command=self.left_click)
        self.button.grid(row=xpos, column=ypos, sticky="ew")

    def left_click(self):
        self.reveal()


class BombCell(Cell):
    def __init__(self):
        super().__init__()
        self.bomb_image = Image.open('resources/bomb.png').resize((BUTTON_SIZE, BUTTON_SIZE))
        self.bomb_image = ImageTk.PhotoImage(self.bomb_image)

    def reveal(self):
        self.hidden = False
        self.to_display=self.bomb_image
        self.button.config(text=None, image=self.to_display)
    
    def create_button(self, frame, xpos, ypos):
        self.button = Button(frame, text=self.to_display, command=self.left_click)
        self.button.grid(row=xpos, column=ypos, sticky="ew")

    def left_click(self):
        self.reveal()


