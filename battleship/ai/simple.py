import random

from grid import Grid


class AI():
    """
    Simple AI
    This AI flags covered fields it knows to be a bomb and
    uncovers fields it knows to not be one. Otherwise it guesses randomly.
    """
    def __init__(self, player_number, own_grid):
        self.player_number = player_number
        self.own_grid = own_grid
        self.enemy_grid = Grid()
        self.current_move = ()

    def make_move(self):
        for ship in self.enemy_grid.ships():
            for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                cell = (ship[0] + direction[0], ship[1] + direction[1])
                if self.enemy_grid.in_grid(*cell) and not self.enemy_grid.is_hit(*cell):
                    self.current_move = cell
                    break
            else:
                continue
            break
        else:
            free_cells = self.enemy_grid.free_cells()
            self.current_move = random.choice(free_cells)

    def end_move(self):
        self.current_move = ()

    def own_hit(self, x, y):
        # Hit on own grid
        self.own_grid.hit(x, y)

    def enemy_hit(self, x, y, is_ship):
        # Hit on enemy grid
        self.enemy_grid.hit(x, y, is_ship)
