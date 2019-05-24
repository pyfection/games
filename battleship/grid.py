import random

import numpy as np
from kivy.event import EventDispatcher


class Grid(EventDispatcher):
    width = 10
    height = 10
    SHIPS = (
        # (Amount, Size)
        (1, 4),  # Battleship
        (2, 3),  # Cruiser
        (3, 2),  # Destroyer
        (4, 1),  # Submarine
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # cells are size of with, height and 2; 2 being bool values for is_hit and is_ship
        self.cells = None
        self.reset()

        self.register_event_type('on_hit')

    def reset(self):
        self.cells = np.zeros((self.width, self.height, 2), dtype=bool)

    def random_init(self):
        def find_cells(size, unchecked):
            for start_cell in unchecked:
                prev_cell = start_cell
                directions = [(1, 0), (0, 1)]
                random.shuffle(directions)
                for direction in directions:
                    cells = []
                    for j in range(size):
                        cell = (prev_cell[0] + direction[0], prev_cell[1] + direction[1])
                        if not self.in_grid(*cell) or self.is_ship(*cell):
                            break
                        prev_cell = cell
                        cells.append(cell)
                    else:
                        return cells

        for ship_type in self.SHIPS:
            amount, size = ship_type
            unchecked = self.free_cells()
            random.shuffle(unchecked)
            for i in range(amount):
                cells = find_cells(size, unchecked)
                for cell in cells:
                    self.place_ship(*cell)


    def in_grid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def adjacent(self, x, y):
        adj = []
        for k in range(x-1, x+2):
            for l in range(y-1, y+2):
                if k == x and l == y:
                    continue
                elif self.in_grid(k, l):
                    adj.append((k, l))
        return adj

    def keys(self):
        return [(w, h) for h in range(self.height) for w in range(self.width)]

    def free_cells(self):
        return [(x, y) for y in range(self.height) for x in range(self.width) if not self.is_hit(x, y)]

    def ships(self):
        return [(x, y) for y in range(self.height) for x in range(self.width) if self.is_ship(x, y)]

    def hit_ships(self):
        return [(x, y)
                for y in range(self.height)
                for x in range(self.width)
                if self.is_ship(x, y) and self.is_hit(x, y)
        ]

    def hit(self, x, y, is_ship=False):
        self.cells[x,y,0] = True
        if is_ship:
            self.place_ship(x, y)
        self.dispatch('on_hit', x, y)

    def place_ship(self, x, y):
        self.cells[x,y,1] = True

    def is_hit(self, x, y):
        return self.cells[x,y,0]

    def is_ship(self, x, y):
        return self.cells[x,y,1]

    def on_hit(self, x, y):
        pass
