"""Game rules and states

This defines the rules of the game and how it behaves.
"""

class Game():
    def __init__(self):
        self.cells = [0 for i in range(9)]
        self.symbol_map = ["_", "x", "o"]
        self.win_patterns = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

    def update(self, cell, player, graphical=False):
        self.cells[cell] = player

        for win_pattern in self.win_patterns:
            comp = win_pattern[0]
            c = self.cells[comp]
            if c == 0:
                continue
            for number in win_pattern[1:]:
                n = self.cells[number]
                if n != c:  # Pattern invalid
                    break
            else:
                return True  # Update is winning move
        return False

    def graphical(self):
        return "\n".join([
            ''.join(
                [self.symbol_map[self.cells[0]], self.symbol_map[self.cells[1]], self.symbol_map[self.cells[2]]]
            ),
            ''.join(
                [self.symbol_map[self.cells[3]], self.symbol_map[self.cells[4]], self.symbol_map[self.cells[5]]]
            ),
            ''.join(
                [self.symbol_map[self.cells[6]], self.symbol_map[self.cells[7]], self.symbol_map[self.cells[8]]]
            )
        ])

    def available_cells(self):
        return [i for i, c in enumerate(self.cells) if c == 0]

    def cells_as_onehot(self, player):
        # onehot is boolean: [unoccupied, me, enemy]
        result = []
        for cell in self.cells:
            if cell == 0:
                result.append(0)
                result.append(0)
            elif cell == 1:
                if player == 1:
                    result.append(1)
                    result.append(0)
                elif player == 2:
                    result.append(0)
                    result.append(1)
            elif cell == 2:
                if player == 1:
                    result.append(0)
                    result.append(1)
                elif player == 2:
                    result.append(1)
                    result.append(0)
        return result

    def is_open(self):
        for win_pattern in self.win_patterns:
            comp = win_pattern[0]
            c = self.cells[comp]
            if c == 0:
                continue
            for number in win_pattern[1:]:
                n = self.cells[number]
                if n != c:
                    break
            else:
                return False
        return bool(self.available_cells())


if __name__ == "__main__":
    game = Game()
    print(game.is_open())
    game.cells[1] = 1
    game.cells[4] = 1
    game.cells[7] = 1
    print(game.is_open())