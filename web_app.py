import streamlit as st
import random
import pickle
from enum import Enum

class Level(Enum):
    BEGINNER = (9, 9, 10)
    MODERATE = (16, 16, 40)
    DIFFICULT = (24, 24, 99)

class Cell:
    def __init__(self):
        self.has_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class Board:
    def __init__(self, level):
        self.rows, self.cols, self.mines = level.value
        self.board = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self._place_mines()
        self._calculate_adjacent_mines()

    def _place_mines(self):
        mine_positions = random.sample(range(self.rows * self.cols), self.mines)
        for pos in mine_positions:
            row, col = divmod(pos, self.cols)
            self.board[row][col].has_mine = True

    def _calculate_adjacent_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.board[row][col].has_mine:
                    self.board[row][col].adjacent_mines = sum(
                        self.board[r][c].has_mine
                        for r in range(max(0, row - 1), min(self.rows, row + 2))
                        for c in range(max(0, col - 1), min(self.cols, col + 2))
                        if (r, c) != (row, col)
                    )

    def reveal_cell(self, row, col):
        if self.board[row][col].is_revealed or self.board[row][col].is_flagged:
            return
        self.board[row][col].is_revealed = True
        if self.board[row][col].adjacent_mines == 0:
            for r in range(max(0, row - 1), min(self.rows, row + 2)):
                for c in range(max(0, col - 1), min(self.cols, col + 2)):
                    if not self.board[r][c].is_revealed:
                        self.reveal_cell(r, c)

    def flag_cell(self, row, col):
        self.board[row][col].is_flagged = not self.board[row][col].is_flagged

def main():
    st.title("Minesweeper")

    if 'board' not in st.session_state:
        st.session_state.board = None
        st.session_state.level = None

    def new_game(level):
        st.session_state.board = Board(level)
        st.session_state.level = level

    def load_game():
        try:
            with open("saved_game.pkl", "rb") as f:
                st.session_state.board = pickle.load(f)
        except FileNotFoundError:
            st.error("No saved game found.")

    def save_game():
        with open("saved_game.pkl", "wb") as f:
            pickle.dump(st.session_state.board, f)
        st.success("Game Saved")

    st.sidebar.title("Menu")
    if st.sidebar.button("New Game"):
        st.session_state.board = None
    if st.sidebar.button("Load Game"):
        load_game()
    
    if st.session_state.board is None:
        st.subheader("Select Difficulty Level")
        if st.button("Beginner"):
            new_game(Level.BEGINNER)
        if st.button("Moderate"):
            new_game(Level.MODERATE)
        if st.button("Difficult"):
            new_game(Level.DIFFICULT)
    else:
        board = st.session_state.board
        for row in range(board.rows):
            cols = st.columns(board.cols)
            for col in range(board.cols):
                cell = board.board[row][col]
                if cell.is_revealed:
                    if cell.has_mine:
                        cols[col].button("*", disabled=True)
                    else:
                        cols[col].button(f"{cell.adjacent_mines}", disabled=True)
                elif cell.is_flagged:
                    cols[col].button("F", key=f"{row}-{col}")
                else:
                    if cols[col].button("", key=f"{row}-{col}"):
                        board.reveal_cell(row, col)
        
        if st.button("Save Game"):
            save_game()

if __name__ == "__main__":
    main()