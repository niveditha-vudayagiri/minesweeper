import tkinter as tk
from Board import Board
from tkinter import messagebox
from tkmacosx import Button
import pickle

class MinesweeperGame(tk.Frame):
    def __init__(self, parent, controller, level=None, board=None):
        super().__init__(parent)
        self.controller = controller
        self.flag_mode = False  # Flag mode state
        if board:
            self.board = board
        else:
            self.board = Board(level)
        self.buttons = [[None for _ in range(self.board.cols)] for _ in range(self.board.rows)]
        self.create_widgets()

    def create_widgets(self):
        self.flag_button = tk.Button(self, text="Click To Enable 🚩 Mode", command=self.toggle_flag_mode, bg="SystemButtonFace")
        self.flag_button.grid(row=0, column=0, columnspan=self.board.cols, pady=10, sticky='ew')

        for r in range(self.board.rows):
            for c in range(self.board.cols):
                btn = tk.Button(self, width=2, height=1, 
                                command=lambda r=r, c=c: self.on_cell_click(r, c))
                btn.grid(row=r+1, column=c)  # Adjust row position to account for the flag button
                self.buttons[r][c] = btn

    def toggle_flag_mode(self):
        self.flag_mode = not self.flag_mode
        self.update_flag_button_color()

    def update_flag_button_color(self):
        if self.flag_mode:
            self.flag_button.config(text="🚩 Mode Enabled!")
        else:
            self.flag_button.config(text="Click To Enable 🚩 Mode!")

    def on_cell_click(self, row, col):
        if self.flag_mode:
            self.flag(row, col)
        else:
            self.reveal(row, col)

    def reveal(self, row, col):
        self.board.reveal_cell(row, col)
        self.update_buttons()
        if self.board.board[row][col].has_mine:
            self.show_all()
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.controller.show_frame('MainMenu')
        elif self.check_win():
            self.show_all()
            messagebox.showinfo("Congratulations", "You win!")
            self.controller.show_frame('MainMenu')

    def flag(self, row, col):
        self.board.flag_cell(row, col)
        self.update_buttons()

    def update_buttons(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.board[r][c]
                btn = self.buttons[r][c]
                if cell.is_revealed:
                    if cell.has_mine:
                        btn.config(text="💣", bg="red")
                    else:
                        btn.config(text=str(cell.adjacent_mines), bg="lightgrey")
                elif cell.is_flagged:
                    btn.config(text="🚩", bg="yellow")
                else:
                    btn.config(text="", bg="SystemButtonFace")

    def show_all(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                self.board.board[r][c].is_revealed = True
        self.update_buttons()

    def check_win(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.board[r][c]
                if not cell.is_revealed and not cell.has_mine:
                    return False
        return True

    def save_game(self):
        with open("saved_game.pkl", "wb") as f:
            pickle.dump(self.board, f)
        messagebox.showinfo("Game Saved", "Your game has been saved.")

    def load_game(self):
        with open("saved_game.pkl", "rb") as f:
            self.board = pickle.load(f)
        self.update_buttons()