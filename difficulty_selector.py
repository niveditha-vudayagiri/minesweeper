import tkinter as tk
from helper_dict import Level
from tkmacosx import Button

class DifficultySelector(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Choose Difficulty Level")
        label.pack(pady=20)

        beginner_button = Button(self, text="Beginner", command=lambda: self.select_level(Level.BEGINNER))
        beginner_button.pack(pady=5)

        moderate_button = Button(self, text="Moderate", command=lambda: self.select_level(Level.MODERATE))
        moderate_button.pack(pady=5)

        difficult_button = Button(self, text="Difficult", command=lambda: self.select_level(Level.DIFFICULT))
        difficult_button.pack(pady=5)

    def select_level(self, level):
        self.controller.initialize_game(level)
        self.controller.show_frame('MinesweeperGame')