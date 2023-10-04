import random
import sys
import time

import numpy as np

from PIL import ImageTk, Image

import tkinter as tk

# Define useful parameters
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540


class SimpleClickGUICanvas:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Simple-Click-GUI-Canvas")
        self.canvas = tk.Canvas(self.window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bd=0)
        self.canvas.pack()
        # Input from user in form of clicks and keyboard
        self.window.bind("<Key>", self.key_input)
        self.window.bind("<Button-1>", self.mouse_input)
        self.play_again()
        self.begin = False


    def initialize_board(self):
        rows = 6
        cols = 6

        boxes_x = 100
        boxes_y = 80
        boxes_w = 50
        boxes_h = 50

        board_line_width = 5
        board_x = boxes_x - board_line_width
        board_y = boxes_y - board_line_width

        boxes_line_width = 3

        l_color_fill = ["#779355", "#ebebd0"]
        l_color_outer = ["#3c571d", "#94957c"]

        for row in range(0, rows):
            for col in range(0, cols):
                idx_color = (row + col) % len(l_color_fill)
                self.own_rectangle(
                    x=boxes_x+col*boxes_w, y=boxes_y+row*boxes_h,
                    w=boxes_w, h=boxes_h, line_width=boxes_line_width,
                    fill=l_color_fill[idx_color], outer=l_color_outer[idx_color],
                )

        self.own_rectangle_outer_only(
            x=board_x, y=board_y,
            w=boxes_w*cols+2*board_line_width, h=boxes_h*rows+2*board_line_width,
            line_width=board_line_width,
            outer="#000000",
        )


    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
    

    def mainloop(self):
        while True:
            self.window.update()


    def mouse_input(self, event):
        pass
        

    def key_input(self, event):
        key_pressed = event.keysym
        print(f"key_pressed: {key_pressed}")


    def own_rectangle_outer_only(self, x, y, w, h, line_width, outer):
        self.canvas.create_rectangle(x, y, x+w, y+line_width, fill=outer, width=0)
        self.canvas.create_rectangle(x, y+h-line_width, x+w, y+h, fill=outer, width=0)
        
        self.canvas.create_rectangle(x, y, x+line_width, y+h, fill=outer, width=0)
        self.canvas.create_rectangle(x+w-line_width, y, x+w, y+h, fill=outer, width=0)


    def own_rectangle(self, x, y, w, h, line_width, fill, outer):
        self.canvas.create_rectangle(x, y, x+w, y+line_width, fill=outer, width=0)
        self.canvas.create_rectangle(x, y+h-line_width, x+w, y+h, fill=outer, width=0)
        
        self.canvas.create_rectangle(x, y, x+line_width, y+h, fill=outer, width=0)
        self.canvas.create_rectangle(x+w-line_width, y, x+w, y+h, fill=outer, width=0)
        
        self.canvas.create_rectangle(x+line_width, y+line_width, x+w-line_width, y+h-line_width, fill=fill, width=0)


game_instance = SimpleClickGUICanvas()
game_instance.mainloop()
