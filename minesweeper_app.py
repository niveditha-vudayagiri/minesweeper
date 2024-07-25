import tkinter as tk
import pickle
from main_menu import MainMenu
from difficulty_selector import DifficultySelector
from minesweeper_game import MinesweeperGame

class MinesweeperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minesweeper")
        self.geometry("400x400")
        self.frames = {}
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.init_main_menu()

    def init_main_menu(self):
        main_menu = MainMenu(parent=self.container, controller=self)
        self.frames["MainMenu"] = main_menu
        main_menu.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainMenu")

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[frame_name]
        frame.grid()

    def start_new_game(self):
        difficulty_selector = DifficultySelector(parent=self.container, controller=self)
        self.frames["DifficultySelector"] = difficulty_selector
        difficulty_selector.grid(row=0, column=0, sticky="nsew")
        self.show_frame("DifficultySelector")

    def initialize_game(self, level):
        self.frames["MinesweeperGame"] = MinesweeperGame(parent=self.container, controller=self, level=level)
        self.frames["MinesweeperGame"].grid(row=0, column=0, sticky="nsew")
        self.resize_to_fit_buttons()
        self.show_frame("MinesweeperGame")

    def load_game(self):
        try:
            with open("saved_game.pkl", "rb") as f:
                board = pickle.load(f)
            self.frames["MinesweeperGame"] = MinesweeperGame(parent=self.container, controller=self, board=board)
            self.frames["MinesweeperGame"].grid(row=0, column=0, sticky="nsew")
            self.show_frame("MinesweeperGame")
        except FileNotFoundError:
            tk.messagebox.showinfo("Error", "No saved game found.")
            self.show_frame("MainMenu")
    
    def resize_to_fit_buttons(self):
        game_frame = self.frames["MinesweeperGame"]
        button_width = 60  # width of a button in pixels
        button_height = 32  # height of a button in pixels
        padding = 20  # additional padding around the buttons

        width = game_frame.board.cols * button_width + padding
        height = game_frame.board.rows * button_height + padding

        self.geometry(f"{width}x{height}")

if __name__ == "__main__":
    app = MinesweeperApp()
    app.mainloop()