import random


class AI():
    """
    Simple AI
    This AI flags covered fields it knows to be a bomb and
    uncovers fields it knows to not be one. Otherwise it guesses randomly.
    """
    def __init__(self, grid):
        self.grid = grid
        self.flagged = set()

    def reload(self):
        self.flagged.clear()

    def solve(self):
        covered = [c for c in self.grid.grid.get_covered() if c not in self.flagged]

        # Flag a cell with bomb
        for cell in covered:
            adjs = self.grid.grid.adjacent(*cell)
            for adj in adjs:
                if self.grid.grid.is_covered(*adj):
                    continue
                bombs = len(self.grid.grid.adjacent_bombs(*adj))
                cov = len([c for c in self.grid.grid.adjacent(*adj) if self.grid.grid.is_covered(*c)])
                if bombs == cov:
                    self.grid.flag(*cell)
                    self.flagged.add(cell)
                    print("Flag cell:", cell)
                    return

        # Uncover cell which can't be a bomb
        for cell in covered:
            adjs = self.grid.grid.adjacent(*cell)
            for adj in adjs:
                if self.grid.grid.is_covered(*adj):
                    continue
                bombs = len(self.grid.grid.adjacent_bombs(*adj))
                flagged = len([f for f in self.grid.grid.adjacent(*adj) if f in self.flagged])
                if bombs == flagged:
                    self.grid.press(*cell)
                    print("Press cell:", cell)
                    return

        # Make random guess
        try:
            cell = random.choice(covered)
        except IndexError:
            print("Nothing more to do")
            return
        self.grid.press(*cell)
        print("Guessed randomly:", cell)