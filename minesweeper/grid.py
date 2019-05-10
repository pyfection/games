import random

import numpy as np


class Grid():
    def __init__(self, bomb_count, width, height):
        self.bomb_count = bomb_count
        self.bombs = np.zeros((width, height), dtype=bool)
        self.covered = np.ones((width, height), dtype=bool)
        self.width = width
        self.height = height

    def reset(self):
        self.bombs = np.zeros((self.width, self.height), dtype=bool)
        self.covered = np.ones((self.width, self.height), dtype=bool)

    def generate(self, empty=()):
        self.reset()
        keys = self.keys()
        for e in empty:
            keys.remove(e)
        for i in range(self.bomb_count):
            key = random.choice(keys)
            keys.remove(key)
            self.bombs[key] = True

    def uncover(self, x, y):
        self.covered[x,y] = False

    def keys(self):
        return [(w, h) for h in range(self.height) for w in range(self.width)]

    def adjacent(self, x, y):
        adj = []
        for k in range(x-1, x+2):
            for l in range(y-1, y+2):
                if k == x and l == y:
                    continue
                elif self.in_grid(k, l):
                    adj.append((k, l))
        return adj

    def adjacent_bombs(self, x, y):
        bombs = []
        for cell in self.adjacent(x, y):
            if self.is_bomb(*cell):
                bombs.append(cell)
        return bombs

    def get_covered(self):
        return [(x, y) for x, y in self.keys() if self.is_covered(x, y)]

    def in_grid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_bomb(self, x, y):
        return self.bombs[x,y]

    def is_covered(self, x, y):
        return self.covered[x,y]

