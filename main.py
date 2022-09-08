from tkinter import *
from PIL import ImageTk, Image
import button_types
from numpy import random

#status bar at top showing num bombs and timer and reset button

COLUMNS = 30
ROWS = 20
DIFFICULTIES = {
    'Easy': 0.1,
    'Medium': 0.2,
    'Hard': 0.3
}
NUM_BOMBS = COLUMNS * ROWS * DIFFICULTIES['Medium']
BOMB_COORDS = set()
ADJACENT_CELLS = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)]
BUTTON_SIZE = 20
IMAGE_SIZE = 18


total_grid = []

def random_num(upper):
    return random.randint(upper)

def generate(frame, flag_image, bad_mark, bomb_image, red_bomb): 
    #rewrite so image generation is in generate function. maybe change get_adjacent to occur only when clicked.
    #make total_grid an instance variable/attribute
    total_grid = [[None for c in range(COLUMNS)] for r in range(ROWS)]
    button_types.Cell.clear_marked()

    BOMB_COORDS.clear()
    while len(BOMB_COORDS) < NUM_BOMBS:
        coord = (random_num(ROWS), random_num(COLUMNS))
        BOMB_COORDS.add(coord)

    for r in range(ROWS):
        for c in range(COLUMNS):
            if (r, c) in BOMB_COORDS:
                new_bomb_cell = button_types.BombCell(total_grid, flag_image, bad_mark, bomb_image, red_bomb)
                new_bomb_cell.create_button(frame, r, c, BOMB_COORDS)
                total_grid[r][c] = new_bomb_cell
            else:
                new_num_cell = button_types.NumCell(total_grid, flag_image, bad_mark)    
                new_num_cell.create_button(frame, r, c)
                total_grid[r][c] = new_num_cell

    for r in range(ROWS):
        for c in range(COLUMNS):
            current_cell = total_grid[r][c]
            current_cell.get_adjacent()
            if isinstance(current_cell, button_types.NumCell):
                current_cell.get_num_bombs()

def main():
    root=Tk()
    root.resizable(height=None, width=None)

    flag_image = Image.open('resources/flag.png').resize\
        ((IMAGE_SIZE, IMAGE_SIZE))
    flag_image = ImageTk.PhotoImage(flag_image)
    bad_mark = Image.open('resources/bad_mark.png').resize\
        ((IMAGE_SIZE, IMAGE_SIZE))
    bad_mark = ImageTk.PhotoImage(bad_mark)
    bomb_image = Image.open('resources/bomb.png').resize\
        ((IMAGE_SIZE, IMAGE_SIZE))
    bomb_image = ImageTk.PhotoImage(bomb_image)
    red_bomb = Image.open('resources/red_bomb.png').resize\
        ((IMAGE_SIZE, IMAGE_SIZE))
    red_bomb = ImageTk.PhotoImage(red_bomb)

    top_frame = Frame(root)
    top_frame.grid(row=0, column=0)

    cell_frame = Frame(root)
    cell_frame.grid(row=1, column=0)

    smiley_image = Image.open('resources/smiley.jpg').resize((BUTTON_SIZE, BUTTON_SIZE))
    smiley_image = ImageTk.PhotoImage(smiley_image)
    new_game_button = Button(top_frame, image=smiley_image, height=BUTTON_SIZE, width=BUTTON_SIZE, command=lambda: generate(cell_frame, flag_image, bad_mark, bomb_image, red_bomb))
    new_game_button.grid(row=0, column=0)

    generate(cell_frame, flag_image, bad_mark, bomb_image, red_bomb)

    root.mainloop()

main()
