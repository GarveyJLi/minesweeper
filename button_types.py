from tkinter import *
from turtle import width
from PIL import ImageTk, Image
from numpy import random

#types of buttons: blank, num, and bomb, reset button
#types of button images: blank, num, bomb, flag, clicked blank, wrong flag, exploded bomb, uncovered


IMAGE_SIZE = 18
BUTTON_SIZE = 2
ADJACENT_CELLS = [(0, 1), (1, 0), (1, 1), (-1, -1), \
    (-1, 0), (0, -1), (1, -1), (-1, 1)]
HIDDEN_TEXT = '   '
marked_cells = []


class Cell:
    def __init__(self, total_grid, flag_image, bad_mark):
        self.marked = False
        self.hidden = True
        self.button = None
        self.xpos = None
        self.ypos = None
        self.adjacent_cells = []
        self.button_frame = None
        self.total_grid = total_grid
        self.bad_mark = bad_mark
        self.flag_image = flag_image
    
    def hide(self):
        self.hidden = True
        self.button.config(image='')
        self.button.config(image=HIDDEN_TEXT)

    def get_adjacent(self):
        rows = len(self.total_grid)
        cols = len(self.total_grid[0])
        for adjacent_cell in ADJACENT_CELLS:
            xpos = self.xpos + adjacent_cell[0]
            ypos = self.ypos + adjacent_cell[1]
            if (xpos >= 0 and xpos < rows) and (ypos >= 0 and ypos < cols):
                self.adjacent_cells.append(self.total_grid[xpos][ypos])
        return self.adjacent_cells

    def get_marked(self):
        return self.marked

    def get_num_marked(self):
        return len(list(filter(lambda x: x.get_marked(), self.adjacent_cells))) 
    
    def toggle_mark(self):
        if not self.marked:
                self.marked = True
                self.button.config(text=HIDDEN_TEXT, image=self.flag_image, width=IMAGE_SIZE)
                marked_cells.append((self.xpos, self.ypos))
        else:
            self.marked = False
            self.button.config(text=HIDDEN_TEXT, image='', width=BUTTON_SIZE)
            marked_cells.remove((self.xpos, self.ypos))

    def toggle_bad_mark(self):
        if self.marked:
            self.marked = False
            self.button.config(text=HIDDEN_TEXT, image=self.bad_mark, width=IMAGE_SIZE)

    def right_click(self, event):
        if self.hidden:
            self.toggle_mark()
        else:
            if isinstance(self, NumCell) and self.num_bombs == self.get_num_marked():
                for cell in self.adjacent_cells:
                    if not cell.get_marked():
                        if isinstance(self, NumCell):
                            if cell.get_num_bombs() == 0:
                                cell.left_click()
                        else:
                            cell.reveal()

    def clear_marked():
        marked_cells = []

class NumCell(Cell):
    def __init__(self, total_grid, flag_image, bad_mark):
        super().__init__(total_grid, flag_image, bad_mark)
        self.adjacent = 0
        self.num_bombs = 0

    def reveal(self):
        if self.hidden:
            self.hidden = False
            self.button.config(image='')
            self.button.config(text=self.num_bombs)
    
    def get_num_bombs(self):
        self.num_bombs = len(list(filter(lambda x: \
            isinstance(x, BombCell), self.adjacent_cells)))
        return self.num_bombs

    def create_button(self, frame, xpos, ypos):
        #self.button_frame = Frame(frame)
        #self.button_frame.grid(row=xpos, column=ypos)
        self.button = Button(frame, text=HIDDEN_TEXT, image='', \
            command=self.left_click, width=BUTTON_SIZE)
        self.button.bind("<Button-3>", self.right_click)
        self.button.grid(row=xpos, column=ypos)
        self.xpos = xpos
        self.ypos = ypos

    def left_click(self):
        if not self.marked:
            if self.hidden:
                if self.num_bombs == 0:
                    self.reveal()
                    for cell in self.adjacent_cells:
                        if not cell.get_marked():
                            cell.left_click()
                else:
                    self.reveal()
            
class BombCell(Cell):
    def __init__(self, total_grid, flag_image, bad_mark, bomb_image, red_bomb):
        super().__init__(total_grid, flag_image, bad_mark)
        self.all_bombs = set()
        self.bomb_image = bomb_image
        self.red_bomb = red_bomb

    def reveal(self):
        self.hidden = False
        self.button.config(text=None, image=self.bomb_image)
    
    def create_button(self, frame, xpos, ypos, all_bombs):
        self.button = Button(frame, text=HIDDEN_TEXT, image='', \
            command=self.left_click)
        self.button.bind("<Button-3>", self.right_click)
        self.button.grid(row=xpos, column=ypos, sticky="nsew")
        self.xpos = xpos
        self.ypos = ypos
        self.all_bombs = all_bombs

    def left_click(self):
        if not self.marked:
            self.hidden = False
            self.button.config(image=self.red_bomb)
            for bomb in self.all_bombs:
                if bomb != (self.xpos, self.ypos):
                    self.total_grid[bomb[0]][bomb[1]].reveal()
            for marked in marked_cells:
                marked_cell = self.total_grid[marked[0]][marked[1]]
                if isinstance(marked_cell, NumCell):
                    marked_cell.toggle_bad_mark()
        marked = []

