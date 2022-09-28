from tkinter import *
from PIL import ImageTk, Image
import button_types
from numpy import random
import sqlite3

DIFFICULTIES = {
    'Easy': 0.1,
    'Medium': 0.15,
    'Hard': 0.2
}
ADJACENT_CELLS = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), \
    (1, -1), (-1, 1)]
BUTTON_SIZE = 20
IMAGE_SIZE = 18

def random_num(upper):
    return random.randint(upper)

def generate(frame, top_frame, \
    rows, columns, bomb_coords, num_nums, total_grid, difficulty_var): 

    total_grid = [[None for c in range(columns)] for r in range(rows)]
    num_bombs = num_nums * DIFFICULTIES[difficulty_var.get()]
    button_types.reset()
    bomb_coords.clear()
    button_types.Cell.num_nums = num_nums
    button_types.Cell.all_bombs = bomb_coords
    button_types.Cell.num_bombs = int(num_bombs)

    while len(bomb_coords) < num_bombs:
        coord = (random_num(rows), random_num(columns))
        bomb_coords.add(coord)
    for r in range(rows):
        for c in range(columns):
            if (r, c) in bomb_coords:
                new_bomb_cell = button_types.BombCell(total_grid)
                new_bomb_cell.create_button(frame, r, c)
                total_grid[r][c] = new_bomb_cell
            else:
                new_num_cell = button_types.NumCell(total_grid)    
                new_num_cell.create_button(frame, r, c)
                total_grid[r][c] = new_num_cell
    for r in range(rows):
        for c in range(columns):
            current_cell = total_grid[r][c]
            current_cell.get_adjacent()
            if isinstance(current_cell, button_types.NumCell):
                current_cell.get_num_bombs()
    button_types.Cell.create_bomb_counter(top_frame)

"""def difficulty_select(frame, difficulty_var, grid_x, grid_y):
    options = OptionMenu(frame, difficulty_var, "Easy", "Medium", "Hard")
    options.grid(row=grid_x, column=grid_y)"""

def user_select(frame, user_var, grid_x, grid_y):
    users = OptionMenu(frame, user_var, "Guest", "New Player")
    users.grid(row=grid_x, column=grid_y)

def submit():
    return

def main():
    root=Tk()
    root.resizable(height=None, width=None)

    root.title('Minesweeper')
    root.iconbitmap('resources/mine.ico')

    conn = sqlite3.connect('player_records.db')
    cur = conn.cursor()

    '''
    cur.execute("""CREATE TABLE records (
        username text,
        games_won integer,
        games_lost integer,
    )""")
    '''

    rows_var = IntVar()
    rows_var.set(10)
    cols_var = IntVar()
    cols_var.set(20)
    difficulty_var = StringVar()
    difficulty_var.set("Easy")
    user_var = StringVar()
    user_var.set("Guest")
    num_nums = rows_var.get() * cols_var.get()
    bomb_coords = set()
    total_grid = []
    
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
    smiley_image = Image.open('resources/smiley.png').resize((BUTTON_SIZE, \
        BUTTON_SIZE))
    smiley_image = ImageTk.PhotoImage(smiley_image)
    win_image = Image.open('resources/sunglasses.png').resize((BUTTON_SIZE, \
        BUTTON_SIZE))
    win_image = ImageTk.PhotoImage(win_image)
    lose_image = Image.open('resources/upside_down.png').resize((BUTTON_SIZE, \
        BUTTON_SIZE))
    lose_image = ImageTk.PhotoImage(lose_image)

    button_types.Cell.flag_image = flag_image
    button_types.Cell.bad_mark = bad_mark
    button_types.Cell.bomb_image = bomb_image
    button_types.Cell.red_bomb = red_bomb
    button_types.Cell.smiley_image = smiley_image
    button_types.Cell.win_image = win_image
    button_types.Cell.lose_image = lose_image
    button_types.Cell.cursor = cur

    top_frame = Frame(root)
    top_frame.grid(row=0, column=0)
    cell_frame = Frame(root)
    cell_frame.grid(row=1, column=0)
    bottom_frame = Frame(root)
    bottom_frame.grid(row=2, column=0)

    new_game_button = Button(top_frame, image=smiley_image, \
        height=BUTTON_SIZE, width=BUTTON_SIZE, command=lambda: \
            generate(cell_frame, top_frame, rows_var.get(), cols_var.get(), bomb_coords, \
                num_nums, total_grid, difficulty_var)) 
    new_game_button.grid(row=0, column=1)
    button_types.Cell.reset_button = new_game_button

    generate(cell_frame, top_frame, rows_var.get(), cols_var.get(), bomb_coords, num_nums, \
            total_grid, difficulty_var)
    

    row_settings = Entry(bottom_frame)
    row_settings.grid(row=0, column=0)
    col_settings = Entry(bottom_frame)
    col_settings.grid(row=0, column=1)
    difficulty_options = OptionMenu(bottom_frame, difficulty_var, "Easy", "Medium", "Hard")
    difficulty_options.grid(row=0, column=3)
    difficulty_select_button = Button(bottom_frame, text="Select", \
        command=lambda:generate(cell_frame, top_frame, rows_var.get(), \
            cols_var.get(), bomb_coords, num_nums, total_grid, \
                difficulty_var))
    difficulty_select_button.grid(row=0, column=4)

    """user_select(bottom_frame, user_var, 0, 1)
    user_select_button = Button(bottom_frame, text="Select", \
        command=lambda:submit())
    user_select_button.grid(row=0, column=2)"""



    conn.commit()
    conn.close()

    root.mainloop()
    
main()
