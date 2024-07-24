from Board import Board

class MinesweeperGame:
    def __init__(self):
        self.board = Board()

    def play(self):
        while True:
            self.board.display_board()

            #Get input from user
            action = input("Enter action (reveal/flag/save/load/quit) and coordinates (row col): ")
            parts = action.split()
            command = parts[0]

            if command == "quit":
                break 

            #Check valid input
            elif command!="save" and command!="reveal" and command!="flag" and command!="load":
                print('Invalid input. Try again!')
                continue

            elif command == "save":
                self.board.save_game(parts[1])
                print("Game saved.")

            elif command == "load":
                self.board = Board.load_game(parts[1])
                print("Game loaded.")

            else:
                row, col = int(parts[1]), int(parts[2])

                if command == "reveal":
                    self.board.reveal_cell(row, col)
                    if self.board.board[row][col].has_mine:
                        self.board.display_board(reveal_all=True)
                        print("Game Over!")
                        break

                elif command == "flag":
                    self.board.flag_cell(row, col)

                if all(cell.is_revealed or (cell.has_mine and cell.is_flagged) for row in self.board.board for cell in row):
                    self.board.display_board(reveal_all=True)
                    print("You Win!")
                    break

if __name__ == "__main__":
    game = MinesweeperGame()
    game.play()