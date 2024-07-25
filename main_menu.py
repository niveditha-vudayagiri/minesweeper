import tkinter as tk
from tkmacosx import Button

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Welcome to Minesweeper")
        label.pack(pady=20)

        new_game_button = Button(self, text="New Game", command=self.start_new_game)
        new_game_button.pack(pady=5)

        load_game_button = Button(self, text="Load Game", command=self.load_game)
        load_game_button.pack(pady=5)

    def start_new_game(self):
        self.controller.start_new_game()

    def load_game(self):
        self.controller.load_game()