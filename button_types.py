from tkinter import *
from PIL import ImageTk, Image
from numpy import random

#types of buttons: blank, num, and bomb, reset button
#types of button images: blank, num, bomb, flag, clicked blank, wrong flag, exploded bomb, uncovered


IMAGE_SIZE = 18
BUTTON_SIZE = 2
ADJACENT_CELLS = [(0, 1), (1, 0), (1, 1), (-1, -1), \
    (-1, 0), (0, -1), (1, -1), (-1, 1)]
marked_cells = []


class Cell:
    def __init__(self):
        self.flag_image = Image.open('resources/flag.png').resize\
            ((IMAGE_SIZE, IMAGE_SIZE))
        self.flag_image = ImageTk.PhotoImage(self.flag_image)
        self.bad_mark = Image.open('resources/bad_mark.png').resize\
            ((IMAGE_SIZE, IMAGE_SIZE))
        self.bad_mark = ImageTk.PhotoImage(self.bad_mark)
        
        self.marked = False
        self.hidden = True
        self.hidden_text = '   '
        self.button = None
        self.to_display = self.hidden_text
        self.xpos = None
        self.ypos = None
        self.adjacent_cells = []
        self.button_frame = None

    
    def hide(self):
        self.hidden = True
        self.to_display = self.hidden_text

    def get_adjacent(self, total_grid):
        for adjacent_cell in ADJACENT_CELLS:
            try:
                single_cell = total_grid[self.xpos + adjacent_cell[0]]\
                    [self.ypos + adjacent_cell[1]]
                if isinstance(single_cell, Cell):
                    self.adjacent_cells.append(single_cell)
            except:
                pass
        return self.adjacent_cells

    def get_marked(self):
        return self.marked

    def get_num_marked(self):
        return len(list(filter(lambda x: x.get_marked(), self.adjacent_cells))) 
    
    def toggle_mark(self):
        if not self.marked:
                self.marked = True
                self.to_display = self.flag_image
                self.button.config(text=self.hidden_text, image=self.to_display)
                marked_cells.append((self.xpos, self.ypos))
        else:
            self.marked = False
            self.to_display = self.hidden_text
            self.button.config(text=self.to_display, image='')
            marked_cells.remove((self.xpos, self.ypos))

    def right_click(self, event):
        if self.hidden:
            self.toggle_mark()
        else:
            if self.num_bombs == self.get_num_marked():
                    for cell in self.adjacent_cells:
                        if not cell.get_marked():
                            if cell.get_num_bombs == 0:
                                cell.left_click()
                            else:
                                cell.reveal()
            
class NumCell(Cell):
    def __init__(self):
        super().__init__()
        self.adjacent = 0
        self.num_bombs = 0

    def reveal(self):
        if self.hidden:
            self.hidden = False
            self.to_display = self.num_bombs
            self.button.config(text=self.to_display)
    
    def get_num_bombs(self):
        self.num_bombs = len(list(filter(lambda x: \
            isinstance(x, BombCell), self.adjacent_cells)))
        return self.num_bombs

    def create_button(self, frame, xpos, ypos):
        #self.button_frame = Frame(frame)
        #self.button_frame.grid(row=xpos, column=ypos)
        self.button = Button(frame, text=self.to_display, \
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
    def __init__(self):
        super().__init__()
        self.bomb_image = Image.open('resources/bomb.png').resize\
            ((IMAGE_SIZE, IMAGE_SIZE))
        self.bomb_image = ImageTk.PhotoImage(self.bomb_image)
        self.red_bomb = Image.open('resources/red_bomb.png').resize\
            ((IMAGE_SIZE, IMAGE_SIZE))
        self.red_bomb = ImageTk.PhotoImage(self.red_bomb)
        self.all_bombs = set()
        self.total_grid = None
        

    def reveal(self):
        self.hidden = False
        self.to_display=self.bomb_image
        self.button.config(text=None, image=self.to_display)
    
    def create_button(self, frame, xpos, ypos, all_bombs, total_grid):
        self.button = Button(frame, text=self.to_display, \
            command=self.left_click)
        self.button.bind("<Button-3>", self.right_click)
        self.button.grid(row=xpos, column=ypos, sticky="nsew")
        self.xpos = xpos
        self.ypos = ypos
        self.all_bombs = all_bombs
        self.total_grid = total_grid

    def left_click(self):
        if not self.marked:
            self.hidden = False
            self.button.config(image=self.red_bomb)
            for bomb in self.all_bombs:
                if bomb != (self.xpos, self.ypos):
                    self.total_grid[bomb[0]][bomb[1]].reveal()
            for marked in marked_cells:
                marked_cell = self.total_grid[marked[0]][marked[1]]
                if isinstance(marked_cell, BombCell):
                    marked_cell.config(image=self.bad_mark)


