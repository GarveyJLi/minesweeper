from hashlib import new
from tkinter import *
from PIL import ImageTk, Image
import button_types
from numpy import random

#status bar at top showing num bombs and timer and reset button

COLUMNS = 30
ROWS = 20
NUM_BOMBS = 15
BOMB_COORDS = set()
ADJACENT_CELLS = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)]

total_grid = []

def random_num(upper):
    return random.randint(upper)

def generate(frame):
    total_grid = [[None for c in range(COLUMNS)] for r in range(ROWS)]

    BOMB_COORDS.clear()
    while len(BOMB_COORDS) < NUM_BOMBS:
        coord = (random_num(ROWS), random_num(COLUMNS))
        BOMB_COORDS.add(coord)

    for r in range(ROWS):
        for c in range(COLUMNS):
            if (r, c) in BOMB_COORDS:
                new_bomb_cell = button_types.BombCell()
                new_bomb_cell.create_button(frame, r, c)
                total_grid[r][c] = new_bomb_cell
            else:
                new_num_cell = button_types.NumCell()    
                new_num_cell.create_button(frame, r, c)
                new_num_cell.get_adjacent
                total_grid[r][c] = new_num_cell

    for r in range(ROWS):
        for c in range(COLUMNS):
            current_cell = total_grid[r][c]
            if isinstance(current_cell, button_types.NumCell):
                current_cell.get_adjacent(total_grid)
                current_cell.get_num_bombs()

def reset():
    return

def main():
    root=Tk()
    root.resizable()

    button_size = 20

    smiley_image = Image.open('resources/smiley.jpg').resize((button_size, button_size))
    smiley_image = ImageTk.PhotoImage(smiley_image)
    #new_game_button = Button(root, image=smiley_image, height=button_size, width=button_size).grid(row=0, column=0)

    generate(root)


                
    root.mainloop()

main()
        
        
        







