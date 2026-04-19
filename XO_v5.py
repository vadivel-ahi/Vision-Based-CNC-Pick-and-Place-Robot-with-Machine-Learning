#! /usr/bin/python3

from math import inf as infinity
from random import choice
from gcode_v3 import *
from image_processing import *
import platform
import time
from os import system

import tkinter as tk
from tkinter import messagebox, simpledialog
from threading import Thread
from random import choice

import serial
ser = serial.Serial('/dev/ttyUSB0', 115200)

HUMAN = -1
COMP = +1
HUMAN_TURNS = +5
COMP_TURNS = +5

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe Game")
        #self.master.geometry("1000x1000")
        self.master.attributes('-fullscreen', True)  # Make the window fullscreen
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(expand=True, fill=tk.BOTH)  # Expand and fill the frame in the window
        self.board_frame.pack()

        self.h_choice = None
        self.first = None

        self.show_welcome_message()

    def show_welcome_message(self):
        welcome_label = tk.Label(self.board_frame, text="Welcome to Tic Tac Toe Game!", font=("Times New Roman Bold", 30))
        welcome_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        rules_label = tk.Label(self.board_frame, text="Rules of the game:", font=("Times New Roman", 20))
        rules_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        rule1_label = tk.Label(self.board_frame, text="1. Select your shape.", font=("Times New Roman", 18))
        rule1_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        rule2_label = tk.Label(self.board_frame, text="2. Choose who starts first.", font=("Times New Roman", 18))
        rule2_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        rule3_label = tk.Label(self.board_frame, text="3. Take turns placing your marks on the grid.", font=("Times New Roman", 18))
        rule3_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        rule4_label = tk.Label(self.board_frame, text="4. Player wins if there are three marks in a row (horizontal, vertical, or diagonal) else the game results in a draw.", font=("Times New Roman", 18))
        rule4_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        play_button = tk.Button(self.board_frame, text="Play", command=self.play_game_setup, font=("Times New Roman", 24))
        play_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        exit_button = tk.Button(self.board_frame, text="Exit", command=self.master.quit, font=("Times New Roman", 24))
        exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def play_game_setup(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        shape_label = tk.Label(self.board_frame, text="Choose a shape:", font=("Times New Roman", 18))
        shape_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Draw Triangle shape
        self.triangle_canvas = tk.Canvas(self.board_frame, width=100, height=100, bg="white", highlightthickness=3, highlightbackground="white")
        self.triangle_canvas.place(relx=0.45, rely=0.4, anchor=tk.CENTER)
        self.triangle_canvas.create_polygon(50, 10, 10, 90, 90, 90, fill="blue")
        self.triangle_canvas.bind("<Button-1>", lambda event: self.select_shape("Triangle"))

        # Draw Circle shape
        self.circle_canvas = tk.Canvas(self.board_frame, width=100, height=100, bg="white", highlightthickness=3, highlightbackground="white")
        self.circle_canvas.place(relx=0.55, rely=0.4, anchor=tk.CENTER)
        self.circle_canvas.create_oval(10, 10, 90, 90, fill="red")
        self.circle_canvas.bind("<Button-1>", lambda event: self.select_shape("Circle"))

        start_label = tk.Label(self.board_frame, text="Choose who starts first:", font=("Times New Roman", 18))
        start_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.start_var = tk.StringVar()
        self.start_var.set("Human")
        self.start_option = tk.OptionMenu(self.board_frame, self.start_var, "Human", "Computer")
        self.start_option.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        start_button = tk.Button(self.board_frame, text="Start Game", command=self.start_game, font=("Times New Roman", 24))
        start_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

    def select_shape(self, shape):
        self.h_choice = shape.upper()
        self.triangle_canvas.config(highlightbackground="white")
        self.circle_canvas.config(highlightbackground="white")
        if shape == "Triangle":
            self.triangle_canvas.config(highlightbackground="black")
        else:
            self.circle_canvas.config(highlightbackground="black")

    def start_game(self):
        self.first = self.start_var.get().upper()
        print(self.first)
        print(self.h_choice)
        if self.first not in ['HUMAN', 'COMPUTER']:
            messagebox.showerror("Error", "Invalid choice for starting first. Please enter Yes or No.")
            return

        if self.h_choice is None:
            messagebox.showerror("Error", "Please select a shape.")
            return

        if self.h_choice == 'TRIANGLE':
            c_choice = 'CIRCLE'
        else:
            c_choice = 'TRIANGLE'

        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.game_thread = Thread(target=self.play_game, args=(self.h_choice, c_choice, self.first))
        self.game_thread.start()

    def play_game(self, h_choice, c_choice, first):
        # Your game logic goes here
        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        
        def empty_cells(state):
            cells = []
            for x, row in enumerate(state):
                for y, cell in enumerate(row):
                    if cell == 0:
                        cells.append([x, y])
            return cells

        def valid_move(x, y):
            if [x, y] in empty_cells(board):
                return True
            else:
                return False

        def set_move(move, x, y, player):
            shape = ''
            gcode = ''
            turn = 0

            global HUMAN_TURNS,COMP_TURNS
            
            if valid_move(x, y):
                board[x][y] = player
                if player == HUMAN:
                    shape = h_shape
                    gcode = position[move]
                    HUMAN_TURNS = HUMAN_TURNS - 1
                    turn = HUMAN_TURNS
                    #print(turn)
                else:
                    shape = c_shape
                    gcode = position[move]
                    COMP_TURNS = COMP_TURNS - 1
                    turn = COMP_TURNS
                time.sleep(5)
                ser.write(shape.encode())
                time.sleep(10)
                Pick_up(turn)
                ser.write(gcode.encode())
                time.sleep(5)
                Drop()
                return True
            else:
                return False

        def wins(state, player):
            win_state = [
                [state[0][0], state[0][1], state[0][2]],
                [state[1][0], state[1][1], state[1][2]],
                [state[2][0], state[2][1], state[2][2]],
                [state[0][0], state[1][0], state[2][0]],
                [state[0][1], state[1][1], state[2][1]],
                [state[0][2], state[1][2], state[2][2]],
                [state[0][0], state[1][1], state[2][2]],
                [state[2][0], state[1][1], state[0][2]],
            ]
            if [player, player, player] in win_state:
                return True
            else:
                return False

        def game_over(state):
            return wins(state, HUMAN) or wins(state, COMP)

        def evaluate(state):
            if wins(state, COMP):
                score = +1
            elif wins(state, HUMAN):
                score = -1
            else:
                score = 0
            return score

        def clean():
            pass

        def human_turn(c_choice, h_choice):

            time.sleep(5)
            ser.write(h_turn.encode())
            time.sleep(5)
            messagebox.showinfo("Tic Tac Toe Game", "Click OK if you have made your move.")

            moves = {
                1: [0, 0], 2: [0, 1], 3: [0, 2],
                4: [1, 0], 5: [1, 1], 6: [1, 2],
                7: [2, 0], 8: [2, 1], 9: [2, 2],
            }
            ser.write(camera.encode())
            time.sleep(5)
            move = shape_detect(h_choice)
            time.sleep(5)
            coord = moves[move]
            board[coord[0]][coord[1]] = HUMAN
            time.sleep(1)

        def ai_turn(c_choice, h_choice):
            moves = {
                1: [0, 0], 2: [0, 1], 3: [0, 2],
                4: [1, 0], 5: [1, 1], 6: [1, 2],
                7: [2, 0], 8: [2, 1], 9: [2, 2],
            }
            depth = len(empty_cells(board))
            if depth == 0 or game_over(board):
                return
            if depth == 9:
                x = choice([0, 1, 2])
                y = choice([0, 1, 2])
            else:
                move = minimax(board, depth, COMP)
                x, y = move[0], move[1]
            for move in moves:
                if moves[move] == [x,y]:
                    break
                else:
                    continue
            set_move(move,x, y, COMP)
            time.sleep(1)

        def minimax(state, depth, player):
            if player == COMP:
                best = [-1, -1, -infinity]
            else:
                best = [-1, -1, +infinity]
            if depth == 0 or game_over(state):
                score = evaluate(state)
                return [-1, -1, score]
            for cell in empty_cells(state):
                x, y = cell[0], cell[1]
                state[x][y] = player
                score = minimax(state, depth - 1, -player)
                state[x][y] = 0
                score[0], score[1] = x, y
                if player == COMP:
                    if score[2] > best[2]:
                        best = score
                else:
                    if score[2] < best[2]:
                        best = score
            return best
            
        def init_game():
            time.sleep(5)
            ser.write(init_gcode.encode())
            time.sleep(5)


        def main():
            global h_shape
            global c_shape
            h_choice = self.h_choice
            first = self.first
            clean()
            init_game()
            # while h_choice != 'TRIANGLE' and h_choice != 'CIRCLE':
            #     try:
            #         print('')
            #         h_choice = simpledialog.askstring("Human Choice", "Choose Triangle or Circle\nChosen: ").upper()
            #     except (EOFError, KeyboardInterrupt):
            #         print('Bye')
            #         exit()
            #     except (KeyError, ValueError):
            #         print('Bad choice')
            if h_choice == 'TRIANGLE':
                c_choice = 'CIRCLE'
                h_shape = Goto_triangle
                c_shape = Goto_circle
            else:
                c_choice = 'TRIANGLE'
                h_shape = Goto_circle
                c_shape = Goto_triangle
            clean() 
            
            while len(empty_cells(board)) > 0 and not game_over(board):
                if first == 'COMPUTER':
                    ai_turn(c_choice, h_choice)
                    first = ''
                human_turn(c_choice, h_choice)
                ai_turn(c_choice, h_choice)
            if wins(board, HUMAN):
                messagebox.showinfo("Game Over", "YOU WIN!")
            elif wins(board, COMP):
                messagebox.showinfo("Game Over", "YOU LOSE!")
            else:
                messagebox.showinfo("Game Over", "DRAW!")
            ser.close()
            exit()

        main()

def main():
    root = tk.Tk()
    tic_tac_toe_gui = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
