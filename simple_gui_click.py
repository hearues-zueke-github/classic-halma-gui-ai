import random
import sys
import time

import numpy as np
import tkinter as tk

from PIL import ImageTk, Image
from tkinter import messagebox

# Define useful parameters
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
BACKGROUND_COLOR = "#1a7e56"

class SimpleClickGUICanvas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple-Click-GUI-Canvas")

        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
            bd=0, insertwidth=0, insertborderwidth=0, selectborderwidth=0, highlightthickness=0, # remove the border from canvas!
        )
        self.canvas.pack()
        self.canvas.configure(bg=BACKGROUND_COLOR)
        # Input from user in form of clicks and keyboard
        self.root.bind("<Key>", self.key_input)
        self.root.bind("<Button-1>", self.mouse_input)
        self.play_again()
        self.is_exit = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)


    def on_exit(self):
        """When you click to exit, this function is called"""
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.is_exit = True


    def initialize_board_variables(self):
        self.rows = 6
        self.cols = 6

        self.boxes_x_min = 100
        self.boxes_y_min = 80
        self.boxes_w = 50
        self.boxes_h = 50

        self.board_line_width = 5
        self.board_x = self.boxes_x_min - self.board_line_width
        self.board_y = self.boxes_y_min - self.board_line_width

        self.boxes_line_width = 3

        self.l_color_fill = ["#779355", "#ebebd0"]
        self.l_color_outer = ["#3c571d", "#94957c"]

        self.boxes_x_max = self.boxes_x_min + self.boxes_w * self.cols
        self.boxes_y_max = self.boxes_y_min + self.boxes_h * self.rows


    def draw_board(self):
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                idx_color = (row + col) % len(self.l_color_fill)
                self.own_rectangle(
                    x=self.boxes_x_min+col*self.boxes_w, y=self.boxes_y_min+row*self.boxes_h,
                    w=self.boxes_w, h=self.boxes_h, line_width=self.boxes_line_width,
                    fill=self.l_color_fill[idx_color], outer=self.l_color_outer[idx_color],
                )

        self.own_rectangle_outer_only(
            x=self.board_x, y=self.board_y,
            w=self.boxes_w*self.cols+2*self.board_line_width, h=self.boxes_h*self.rows+2*self.board_line_width,
            line_width=self.board_line_width,
            outer="#000000",
        )


    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board_variables()
        self.draw_board()
    

    def mainloop(self):
        while not self.is_exit:
            self.root.update()


    # TODO: add a board matrix and check if a tile is clicked already for the beginning
    def mouse_input(self, event):
        pos_x = event.x
        pos_y = event.y
        print(f"clicked at: {{pos_x: {pos_x}, pos_y: {pos_y}}}")

        # calculate the center of one border tile/box
        # if it is ouside the tile, return none
        if not (
            (pos_x >= self.boxes_x_min) and (pos_x < self.boxes_x_max) and
            (pos_y >= self.boxes_y_min) and (pos_y < self.boxes_y_max)
        ):
            print("- Missed the tiles!")
            return

        tile_x = (pos_x - self.boxes_x_min) // self.boxes_w
        tile_y = (pos_y - self.boxes_y_min) // self.boxes_h

        pos_tile_x_mid = self.boxes_x_min + self.boxes_w // 2 + tile_x * self.boxes_w
        pos_tile_y_mid = self.boxes_y_min + self.boxes_h // 2 + tile_y * self.boxes_h

        radius = (self.boxes_w * 0.6) // 2
        x1 = pos_tile_x_mid - radius
        y1 = pos_tile_y_mid - radius
        x2 = pos_tile_x_mid + radius
        y2 = pos_tile_y_mid + radius

        color = '#' + ''.join([f'{val:02x}' for val in np.random.randint(0x40, 0xC0, (3, ))])
        self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=color, width=2)
        

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
