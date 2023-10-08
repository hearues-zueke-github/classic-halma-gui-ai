import random
import sys
import time

import numpy as np
import tkinter as tk

from PIL import ImageTk, Image
from tkinter import messagebox

from tkextrafont import Font

# Define useful parameters
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
BACKGROUND_COLOR = "#1a7e56"

class Piece:
    def __init__(self, player_nr, piece_nr):
        self.player_nr = player_nr
        self.piece_nr = piece_nr
        self.tile_y = tile_y
        self.tile_x = tile_x


class Player:
    def __init__(self, player_nr, color, l_piece_pos):
        self.player_nr = player_nr
        self.color = color
        self.l_piece_pos = l_piece_pos


class SimpleClickGUICanvas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple-Click-GUI-Canvas")

        self.my_font = Font(file="BPdots/BPdotsSquareBold.otf", family="BPdots")

        self.root.config(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
            bd=0, insertwidth=0, insertborderwidth=0, selectborderwidth=0, highlightthickness=0, # remove the border from canvas!
        )
        self.canvas.place(x=0, y=0)
        self.canvas.configure(bg=BACKGROUND_COLOR)

        # Input from user in form of clicks and keyboard
        self.canvas.bind("<Key>", self.key_input)
        self.canvas.bind("<Button-1>", self.mouse_input)
        self.play_again()
        self.is_exit = False

        self.frame_text_main = tk.Frame(self.root, height=400, width=300)
        self.frame_text_main.place(x=self.boxes_x_max + self.board_line_width + 20, y=20)
        self.frame_text_main.pack_propagate(0)

        self.text_main = tk.Text(self.frame_text_main, bg='#364060', fg='#96d9a9', font=self.my_font)
        # self.text_main.pack(fill="both", expand=True, padx=0, pady=0)

        self.scrollbar = tk.Scrollbar(self.frame_text_main)
        self.scrollbar.config(command=self.text_main.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_main.pack(side="left")

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)


    def on_exit(self):
        """When you click to exit, this function is called"""
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.is_exit = True


    def initialize_board_variables(self):
        self.rows = 6
        self.cols = 6
        self.amount_player = 2
        self.amount_pieces_per_player = 3

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

        self.arr_board = np.zeros((self.rows, self.cols), dtype=np.uint8)

        self.l_player_l_piece = [
            [
                Piece(player_nr=0, piece_nr=0, tile_y=0, tile_x=0),
                Piece(player_nr=0, piece_nr=1, tile_y=0, tile_x=1),
                Piece(player_nr=0, piece_nr=2, tile_y=1, tile_x=0),
            ],
            [
                Piece(player_nr=1, piece_nr=3, tile_y=self.rows-1, tile_x=self.cols-1),
                Piece(player_nr=1, piece_nr=4, tile_y=self.rows-1, tile_x=self.cols-2),
                Piece(player_nr=1, piece_nr=5, tile_y=self.rows-2, tile_x=self.cols-1),
            ],
        ]
        # init pieces for now hardcoded
        self.d_tile_to_piece_obj = {}
        self.d_piece_nr_to_tile = {}


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
        pos_y = event.y
        pos_x = event.x
        print(f"event: {event}")
        print(f"clicked at: {{pos_y: {pos_y}, pos_x: {pos_x}}}")

        # calculate the center of one border tile/box
        # if it is ouside the tile, return none
        if not (
            (pos_y >= self.boxes_y_min) and (pos_y < self.boxes_y_max) and
            (pos_x >= self.boxes_x_min) and (pos_x < self.boxes_x_max)
        ):
            print("- Missed the tiles!")
            return

        tile_y = (pos_y - self.boxes_y_min) // self.boxes_h
        tile_x = (pos_x - self.boxes_x_min) // self.boxes_w

        if self.arr_board[tile_y, tile_x] != 0:
            print(f"Already clicked on tile ({tile_y}, {tile_x})!")
            return

        self.arr_board[tile_y, tile_x] = 1

        pos_tile_y_mid = self.boxes_y_min + self.boxes_h // 2 + tile_y * self.boxes_h
        pos_tile_x_mid = self.boxes_x_min + self.boxes_w // 2 + tile_x * self.boxes_w

        radius = (self.boxes_w * 0.6) // 2
        y1 = pos_tile_y_mid - radius
        x1 = pos_tile_x_mid - radius
        y2 = pos_tile_y_mid + radius - 1
        x2 = pos_tile_x_mid + radius - 1

        color = '#' + ''.join([f'{val:02x}' for val in np.random.randint(0x40, 0xC0, (3, ))])
        self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=color, width=2)

        self.text_main.insert(tk.INSERT, f"tile_clicked: ({tile_y}, {tile_x})\n")
        self.text_main.see("end")
        

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
