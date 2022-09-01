from tkinter import *

#types of buttons: blank, num, and bomb, reset button
#types of button images: blank, num, bomb, flag, clicked blank, wrong flag, exploded bomb, uncovered


class Cell:
    def __init__(self, frame, xpos, ypos):
        self.hidden = True
        self.button = Button(frame)
        self.button.grid(row=xpos, column=ypos, sticky="ew")
        #self.button.bind("<Button-3>", right_click())

        def right_click(self, event):
            #self.config(text='', background=)
            return


class NumCell(Cell):
    def __init__(self, frame, xpos, ypos):
        super().__init__(frame, xpos, ypos)
        self.adjacent = 0
    
    def add_adjacent(self):
        self.adjacent += 1

    def set_val(self):
        self.button.config(text=self.add_adjacent)


class BombCell(Cell):
    def __init__(self, frame, xpos, ypos):
        super().__init__(frame, xpos, ypos)
        self.button.config(text='B')
