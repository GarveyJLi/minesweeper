from tkinter import *
from PIL import ImageTk, Image
import button_types
from numpy import random

#types of buttons: blank, num, and bomb, reset button
#types of button images: blank, num, bomb, flag, clicked blank, wrong flag, exploded bomb, uncovered


BUTTON_SIZE = 20
ADJACENT_CELLS = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)]


class Cell:
    def __init__(self):
        self.hidden = True
        self.hidden_text = '   '
        self.button = None
        self.to_display = self.hidden_text
        self.xpos = 0
        self.ypos = 0
        #self.button.bind("<Button-3>", right_click())
    
    def hide(self):
        self.hidden = True
        self.to_display = self.hidden_text



class NumCell(Cell):
    def __init__(self):
        super().__init__()
        self.adjacent = 0
        self.adjacent_cells = []
        self.num_bombs = 0

    def reveal(self):
        self.hidden = False
        self.to_display = self.num_bombs
        self.button.config(text=self.to_display)

    def get_adjacent(self, total_grid):
        for adjacent_cell in ADJACENT_CELLS:
            try:
                single_cell = total_grid[self.xpos + adjacent_cell[0]][self.ypos + adjacent_cell[1]]
                self.adjacent_cells.append(single_cell)
            except:
                pass
        return
    
    def get_num_bombs(self):
        self.num_bombs = len(list(filter(lambda x: isinstance(x, BombCell), self.adjacent_cells)))
        return self.num_bombs

    def set_val(self):
        self.button.config(text=self.to_display)

    def create_button(self, frame, xpos, ypos):
        self.button = Button(frame, text=self.to_display, command=self.left_click)
        self.button.grid(row=xpos, column=ypos, sticky="ew")
        self.xpos = xpos
        self.ypos = ypos

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
        self.xpos = xpos
        self.ypos = ypos

    def left_click(self):
        self.reveal()


