from Cell import Cell
from helper_dict import *
import random
import pickle

class Board:
    def __init__(self, level):
        self.chooseDifficultyLevel(level)

        self.board = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self._place_mines()
        self._calculate_adjacent_mines()

    #Function to choose difficult level
    def chooseDifficultyLevel(self,level):
        if(level==Level.BEGINNER):
            self.rows = 9
            self.cols = 9
            self.mines = 10
        elif(level==Level.MODERATE):
            self.rows = 16
            self.cols = 16
            self.mines = 40
        elif(level==Level.DIFFICULT):
            self.rows = 24
            self.cols = 24
            self.mines = 99
        else:
            self.rows = 5
            self.cols = 5
            self.mines = 5

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

    # def display_board(self, reveal_all=False):
    #     print("- "*self.cols)

    #     for row in self.board:
    #         for cell in row:
    #             if reveal_all:
    #                 cell.is_revealed = True
    #             print(cell, end=' ')
    #         print()
        
    #     print("- "*self.cols)