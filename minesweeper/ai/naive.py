

class AI():
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        covered = self.grid.grid.get_covered()
        try:
            cell = covered[0]
        except IndexError:
            print("Nothing more to do")
            return
        self.grid.press(*cell)
        print("Press", cell)