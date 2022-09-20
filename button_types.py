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

def timer_start_end():
    if Cell.game_start and not Cell.game_end:
        return True
    return False

def reset():
    Cell.num_clicked = 0
    Cell.game_start = False
    Cell.game_end = False
    Cell.game_win = None
    Cell.marked_cells = []
    Cell.clickable = True

class Cell:
    bomb_counter = None
    num_bombs = 0
    marked_cells = []
    num_clicked = 0
    num_nums = 0
    clickable = True
    game_start = False
    game_end = False
    game_win = None
    reset_button = None
    all_bombs = None

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
                self.button.config(text=HIDDEN_TEXT, image=self.flag_image, \
                    width=IMAGE_SIZE)
                Cell.marked_cells.append((self.xpos, self.ypos))
        else:
            self.marked = False
            self.button.config(text=HIDDEN_TEXT, image='', width=BUTTON_SIZE)
            Cell.marked_cells.remove((self.xpos, self.ypos))

    def toggle_bad_mark(self):
        if self.marked:
            self.marked = False
            self.button.config(text=HIDDEN_TEXT, image=self.bad_mark, \
                width=IMAGE_SIZE)

    def right_click(self, event):
        if Cell.clickable:
            if self.hidden:
                self.toggle_mark()
                Cell.bomb_counter.config(text=(Cell.num_bombs - \
                    len(Cell.marked_cells)))
            else:
                if isinstance(self, NumCell) and (self.num_bombs == \
                    self.get_num_marked()):
                    for cell in self.adjacent_cells:
                        if not cell.get_marked():
                            if isinstance(cell, NumCell):
                                if cell.get_num_bombs() == 0:
                                    cell.left_click()
                                else:
                                    cell.reveal()
                            else:
                                cell.left_click()
                            print(Cell.num_clicked)


    @staticmethod
    def game_win():
        Cell.clickable = False
        Cell.game_end = True
        Cell.game_win = True
        print("win")
        return

    @staticmethod
    def game_lose():
        Cell.clickable = False
        Cell.game_end = True
        Cell.game_win = False
        print('lose')
        return

    @staticmethod
    def create_bomb_counter(frame):
        Cell.bomb_counter = Label(frame, text=(Cell.num_bombs - \
            len(Cell.marked_cells)))
        Cell.bomb_counter.grid(row=0, column=0)

class NumCell(Cell):
    def __init__(self, total_grid, flag_image, bad_mark):
        super().__init__(total_grid,  flag_image, bad_mark)
        self.adjacent = 0
        self.num_bombs = 0

    def reveal(self):
        if self.hidden:
            self.hidden = False
            self.button.config(image='')
            self.button.config(text=self.num_bombs)
            Cell.num_clicked += 1
        if Cell.num_clicked + Cell.num_bombs == Cell.num_nums:
            Cell.game_win()
    
    def get_num_bombs(self):
        self.num_bombs = len(list(filter(lambda x: \
            isinstance(x, BombCell), self.adjacent_cells)))
        return self.num_bombs

    def create_button(self, frame, xpos, ypos):
        self.button = Button(frame, text=HIDDEN_TEXT, image='', \
            command=self.left_click, width=BUTTON_SIZE)
        self.button.bind("<Button-3>", self.right_click)
        self.button.grid(row=xpos, column=ypos)
        self.xpos = xpos
        self.ypos = ypos

    def left_click(self):
        if Cell.clickable:
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
    def __init__(self, total_grid, flag_image, bad_mark, \
        bomb_image, red_bomb):
        super().__init__(total_grid, flag_image, bad_mark)
        self.bomb_image = bomb_image
        self.red_bomb = red_bomb

    def reveal(self):
        self.hidden = False
        self.button.config(text=None, image=self.bomb_image)
    
    def create_button(self, frame, xpos, ypos):
        self.button = Button(frame, text=HIDDEN_TEXT, image='', \
            command=self.left_click)
        self.button.bind("<Button-3>", self.right_click)
        self.button.grid(row=xpos, column=ypos, sticky="nsew")
        self.xpos = xpos
        self.ypos = ypos

    def left_click(self):
        if Cell.clickable:
            if not self.marked:
                self.hidden = False
                self.button.config(image=self.red_bomb)
                for bomb in Cell.all_bombs:
                    if bomb != (self.xpos, self.ypos):
                        self.total_grid[bomb[0]][bomb[1]].reveal()
                for marked in Cell.marked_cells:
                    marked_cell = self.total_grid[marked[0]][marked[1]]
                    if isinstance(marked_cell, NumCell):
                        marked_cell.toggle_bad_mark()
                Cell.game_lose()


