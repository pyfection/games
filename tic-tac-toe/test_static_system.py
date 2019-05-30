"""Test of a hardcoded AI

This AI is quite good, but not perfect.
"""

import random


class StaticSystem():
    """
    Inputs:
    0 (1:1 Available)
    1 (1:1 Me)
    2 (1:1 Enemy)
    3 (2:1 Available)
    4 (2:1 Me)
    5 (2:1 Enemy)
    6 (3:1 Available)
    7 (3:1 Me)
    8 (3:1 Enemy)
    9 (1:2 Available)
    10 (1:2 Me)
    11 (1:2 Enemy)
    12 (2:2 Available)
    13 (2:2 Me)
    14 (2:2 Enemy)
    15 (3:2 Available)
    16 (3:2 Me)
    17 (3:2 Enemy)
    18 (1:3 Available)
    19 (1:3 Me)
    20 (1:3 Enemy)
    21 (2:3 Available)
    22 (2:3 Me)
    23 (2:3 Enemy)
    24 (3:3 Available)
    25 (3:3 Me)
    26 (3:3 Enemy)
    """
    w_occupied = 0
    w_available = .1
    w_potential_block = 1
    w_potential_finish = 10
    w_block = 100
    w_finish = 1000
    # connections (input, output): weight
    # connections = {
    #     # Don't place where is already placed
    #     (1, 0): w_occupied,
    #     (2, 0): w_occupied,
    #     (4, 1): w_occupied,
    #     (5, 1): w_occupied,
    #     (7, 2): w_occupied,
    #     (8, 2): w_occupied,
    #     (10, 3): w_occupied,
    #     (11, 3): w_occupied,
    #     (13, 4): w_occupied,
    #     (14, 4): w_occupied,
    #     (16, 5): w_occupied,
    #     (17, 5): w_occupied,
    #     (19, 6): w_occupied,
    #     (20, 6): w_occupied,
    #     (22, 7): w_occupied,
    #     (23, 7): w_occupied,
    #     (25, 8): w_occupied,
    #     (26, 8): w_occupied,
    #     # Winning Move
    #     (4, 0): w_finish, (7, 0): w_finish, (10, 0): w_finish, (13, 0): w_finish, (19, 0): w_finish, (25, 0): w_finish,
    #     (1, 1): w_finish, (7, 1): w_finish, (13, 1): w_finish, (22, 1): w_finish,
    #     (1, 2): w_finish, (4, 2): w_finish, (13, 2): w_finish, (16, 2): w_finish, (19, 2): w_finish, (25, 2): w_finish,
    #     (1, 3): w_finish, (13, 3): w_finish, (16, 3): w_finish, (19, 3): w_finish,
    #     (1, 4): w_finish, (4, 4): w_finish, (7, 4): w_finish, (10, 4): w_finish, (16, 4): w_finish, (19, 4): w_finish, (22, 4): w_finish, (25, 4): w_finish,
    #     (7, 5): w_finish, (10, 5): w_finish, (13, 5): w_finish, (25, 5): w_finish,
    #     (1, 6): w_finish, (7, 6): w_finish, (10, 6): w_finish, (13, 6): w_finish, (22, 6): w_finish, (25, 6): w_finish,
    #     (4, 7): w_finish, (13, 7): w_finish, (19, 7): w_finish, (25, 7): w_finish,
    #     (1, 8): w_finish, (7, 8): w_finish, (13, 8): w_finish, (16, 8): w_finish, (19, 8): w_finish, (22, 8): w_finish,
    #     # Potential Winning
    #     (4, 0): w_finish, (7, 0): w_finish, (10, 0): w_finish, (13, 0): w_finish, (19, 0): w_finish, (25, 0): w_finish,
    #     (1, 1): w_finish, (7, 1): w_finish, (13, 1): w_finish, (22, 1): w_finish,
    #     (1, 2): w_finish, (4, 2): w_finish, (13, 2): w_finish, (16, 2): w_finish, (19, 2): w_finish, (25, 2): w_finish,
    #     (1, 3): w_finish, (13, 3): w_finish, (16, 3): w_finish, (19, 3): w_finish,
    #     (1, 4): w_finish, (4, 4): w_finish, (7, 4): w_finish, (10, 4): w_finish, (16, 4): w_finish, (19, 4): w_finish, (22, 4): w_finish, (25, 4): w_finish,
    #     (7, 5): w_finish, (10, 5): w_finish, (13, 5): w_finish, (25, 5): w_finish,
    #     (1, 6): w_finish, (7, 6): w_finish, (10, 6): w_finish, (13, 6): w_finish, (22, 6): w_finish, (25, 6): w_finish,
    #     (4, 7): w_finish, (13, 7): w_finish, (19, 7): w_finish, (25, 7): w_finish,
    #     (1, 8): w_finish, (7, 8): w_finish, (13, 8): w_finish, (16, 8): w_finish, (19, 8): w_finish, (22, 8): w_finish,
    #     # Bonus for blocking enemy
    #     (5, 0): w_block, (8, 0): w_block, (11, 0): w_block, (14, 0): w_block, (20, 0): w_block, (26, 0): w_block,
    #     (2, 1): w_block, (8, 1): w_block, (14, 1): w_block, (23, 1): w_block,
    #     (2, 2): w_block, (5, 2): w_block, (14, 2): w_block, (17, 2): w_block, (20, 2): w_block, (26, 2): w_block,
    #     (2, 3): w_block, (14, 3): w_block, (17, 3): w_block, (20, 3): w_block,
    #     (2, 4): w_block, (5, 4): w_block, (8, 4): w_block, (11, 4): w_block, (17, 4): w_block, (20, 4): w_block, (23, 4): w_block, (26, 4): w_block,
    #     (8, 5): w_block, (11, 5): w_block, (14, 5): w_block, (26, 5): w_block,
    #     (2, 6): w_block, (8, 6): w_block, (11, 6): w_block, (14, 6): w_block, (23, 6): w_block, (26, 6): w_block,
    #     (5, 7): w_block, (14, 7): w_block, (20, 7): w_block, (26, 7): w_block,
    #     (2, 8): w_block, (8, 8): w_block, (14, 8): w_block, (17, 8): w_block, (20, 8): w_block, (23, 8): w_block,
    # }
    connections = {
        0: (w_available, w_available, w_available),  # 00 00 00
        1: (w_potential_finish, w_potential_finish, w_occupied),  # 00 00 01
        2: (w_potential_block, w_potential_block, w_occupied),  # 00 00 10
        4: (w_potential_finish, w_occupied, w_potential_finish),  # 00 01 00
        5: (w_finish, w_occupied, w_occupied),  # 00 01 01
        6: (w_available, w_occupied, w_occupied),  # 00 01 10
        8: (w_potential_block, w_occupied, w_potential_block),  # 00 10 00
        9: (w_available, w_occupied, w_occupied),  # 00 10 01
        10: (w_block, w_occupied, w_occupied),  # 00 10 10
        16: (w_occupied, w_potential_finish, w_potential_finish),  # 01 00 00
        17: (w_occupied, w_finish, w_occupied),  # 01 00 01
        18: (w_occupied, w_available, w_occupied),  # 01 00 10
        20: (w_occupied, w_occupied, w_finish),  # 01 01 00
        21: (w_occupied, w_occupied, w_occupied),  # 01 01 01
        22: (w_occupied, w_occupied, w_occupied),  # 01 01 10
        24: (w_occupied, w_occupied, w_available),  # 01 10 00
        25: (w_occupied, w_occupied, w_occupied),  # 01 10 01
        26: (w_occupied, w_occupied, w_occupied),  # 01 10 10
        32: (w_occupied, w_potential_block, w_potential_block),  # 10 00 00
        33: (w_occupied, w_available, w_occupied),  # 10 00 01
        34: (w_occupied, w_block, w_occupied),  # 10 00 10
        36: (w_occupied, w_occupied, w_available),  # 10 01 00
        37: (w_occupied, w_occupied, w_occupied),  # 10 01 01
        38: (w_occupied, w_occupied, w_occupied),  # 10 01 10
        40: (w_occupied, w_occupied, w_block),  # 10 10 00
        41: (w_occupied, w_occupied, w_occupied),  # 10 10 01
        42: (w_occupied, w_occupied, w_occupied),  # 10 10 10
    }
    win_rows = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    def activate(self, inputs):
        outputs = [0 for _ in range(9)]
        if sum(inputs) == 0:
            outputs[random.choice((0, 2, 6, 8))] = 1
            return outputs
        for row in self.win_rows:
            s = ''
            for cell in row:
                me_cell = inputs[cell*2]
                en_cell = inputs[cell*2+1]
                s += str(me_cell) + str(en_cell)
            key = int(s, base=2)
            for i, cell in enumerate(row):
                outputs[cell] += self.connections[key][i]
        return outputs

        # outputs = [0 for _ in range(9)]
        # for con, weight in self.connections.items():
        #     i, o = con
        #     try:
        #         outputs[o] += inputs[i] * weight
        #     except IndexError:
        #         print(i, o)
        #         raise
        # return outputs


if __name__ == "__main__":
    from game import Game
    # net = StaticSystem()
    # inp = [0 for _ in range(18)]
    # print(net.activate(inp))

    # Player test
    net = StaticSystem()
    while True:
        game = Game()
        current_player = int(input("First player ([1] or 2): ") or 1)
        while game.available_cells():
            if current_player == 1:
                output = 0
                while not output:
                    output = int(input("Cell (1-9): "))
                    if output-1 not in game.available_cells():
                        print("Can't place there, try again!")
                        output = 0
                output -= 1
            else:
                output = net.activate(game.cells_as_onehot(current_player))
                print(output)
                output = max(enumerate(output), key=lambda p: p[1])[0]
            winning_move = game.update(output, current_player)
            if winning_move:
                if current_player == 1:
                    print("Congratulations, you won!")
                else:
                    print("Aw you lost, better luck next time!")
                break

            current_player = 1 if current_player == 2 else 2

            print("\n" + game.graphical())
        print("\n" + game.graphical())

        if not bool(input("Another turn? (0|1): ")):
            break