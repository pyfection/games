"""Play a game against the best Network

Enter a number in the terminal to place your symbol.
The network you play against was the best network from main.py
"""

import os
import pickle

import neat

from game import Game


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(
    neat.DefaultGenome, neat.DefaultReproduction,
    neat.DefaultSpeciesSet, neat.DefaultStagnation,
    config_path
)
with open('winner.pck', 'r') as f:
    winner = pickle.load(f)

game = Game()
net = neat.nn.FeedForwardNetwork.create(winner, config)
print("You are player 1 and have 'x'")

while True:
    current_player = int(input("First player ([1] or 2): ")) or 1
    while game.available_cells():
        if current_player == 1:
            output = 0
            while not output:
                output = int(input("Cell (1-9): "))
                if output not in game.available_cells():
                    print("Can't place there, try again!")
                    output = 0
        else:
            output = net.activate(game.cells_as_onehot(current_player))
            original_output = max(enumerate(output), key=lambda p: p[1])[0]
            output = [o if i in game.available_cells() else 0 for i, o in enumerate(output)]
            output = max(enumerate(output), key=lambda p: p[1])[0]
            if original_output != output:
                print("(Enemy originally wanted to place on field", original_output, ")")
        winning_move = game.update(output, current_player)
        if winning_move:
            if current_player == 1:
                print("Congratulations, you won!")
            else:
                print("Aw you lost, better luck next time!")
            break

        current_player = 1 if current_player == 2 else 2

    if bool(input("Another turn? (0|1): ")):
        break