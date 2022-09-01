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

    def create_button(self, frame, xpos, ypos):
        self.button = Button(frame)
        self.button.grid(row=xpos, column=ypos, sticky="ew")

class NumCell(Cell):
    def __init__(self, frame, xpos, ypos):
        super().__init__(frame, xpos, ypos)
        self.adjacent = 0
        self.button.config(text=self.to_display)
        
    def toggle_hidden(self):
        if self.hidden:
            self.hidden = False
            self.to_display = self.adjacent
        else:
            self.hidden = True
            self.to_display = self.hidden_text


    def add_adjacent(self):
        self.adjacent += 1

    def set_val(self):
        self.button.config(text=self.adjacent)




class BombCell(Cell):
    def __init__(self, frame, xpos, ypos):
        super().__init__(frame, xpos, ypos)
        self.bomb_image = Image.open('resources/bomb.png').resize((BUTTON_SIZE, BUTTON_SIZE))
        self.bomb_image = ImageTk.PhotoImage(self.bomb_image)
        self.button.config(text=self.to_display)

    def toggle_hidden(self):
        if self.hidden:
            self.hidden = False
            self.to_display=self.bomb_image
        else:
            self.hidden = True
            self.to_display = self.hidden_text

