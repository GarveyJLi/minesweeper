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

def random_num(upper):
    return random.randint(upper)

def generate():
    BOMB_COORDS.clear()
    while len(BOMB_COORDS) < NUM_BOMBS:
        coord = (random_num(ROWS), random_num(COLUMNS))
        BOMB_COORDS.add(coord)

def reset():
    return

def main():
    root=Tk()
    root.resizable()

    button_size = 20

    smiley_image = Image.open('resources/smiley.jpg').resize((button_size, button_size))
    smiley_image = ImageTk.PhotoImage(smiley_image)
    #new_game_button = Button(root, image=smiley_image, height=button_size, width=button_size).grid(row=0, column=0)

    generate()

    for bomb_coord in BOMB_COORDS:
        new_bomb_cell = button_types.BombCell(root, bomb_coord[0], bomb_coord[1])

    for c in range(COLUMNS):
        for r in range(ROWS):
            if (r, c) not in BOMB_COORDS:
                new_num_cell = button_types.NumCell(root, r, c)    
                for adjacent_cell in ADJACENT_CELLS:
                    if (r + adjacent_cell[0], c + adjacent_cell[1]) in BOMB_COORDS:
                        new_num_cell.add_adjacent()
                
    root.mainloop()

main()
        
        
        







