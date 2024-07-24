class Cell:
    def __init__(self, has_mine=False):
        self.has_mine = has_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def __repr__(self):
        if self.is_flagged:
            return 'F'
        elif not self.is_revealed:
            return ' '
        elif self.has_mine:
            return '*'
        else:
            return str(self.adjacent_mines)