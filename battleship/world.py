from grid import Grid


LOCAL_PLAYER = 0
AI_PLAYER = 1


class World:
    def __init__(self):
        self.grids = [
            Grid(),
            Grid()
        ]
        for grid in self.grids:
            grid.random_init()