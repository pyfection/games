"""9-input Tic-Tac-Toe Game

"""

from __future__ import print_function
import os
import pickle
import neat
from game import Game
from test_static_system import StaticSystem
import visualize


def eval_genomes(genomes, config):
    contestant = StaticSystem()
    for genome_id, genome in genomes:
        genome.fitness = 0
        genome.wins = 0
        genome.fouls = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        max_turns = 200
        for turn in range(max_turns):
            # opponent_moves = list(range(9))
            # random.shuffle(opponent_moves)
            game = Game()
            current_contestant = 1 #turn % 2 + 1
            while game.available_cells():
                output = None
                if current_contestant == 1:
                    output = net.activate(game.cells_as_onehot(current_contestant))
                    # output = [o if i in game.available_cells() else 0 for i, o in enumerate(output)]
                    output = max(enumerate(output), key=lambda p: p[1])[0]
                else:
                    # for i, move in enumerate(opponent_moves):
                    #     if move in game.available_cells():
                    #         output = opponent_moves.pop(i)
                    #         break
                    # else:
                    #     raise ValueError("Opponent should always have a move")
                    output = contestant.activate(game.cells_as_onehot(current_contestant))
                    output = max(enumerate(output), key=lambda p: p[1])[0]
                if output not in game.available_cells():
                    genome.fitness -= 1  # Player fouled
                    break
                winning_move = game.update(output, current_contestant)
                if winning_move:
                    if current_contestant == 1:
                        genome.fitness += 1  # Player won
                    break

                current_contestant = 1 if current_contestant == 2 else 2
                # Bonus for completing a turn
                genome.fitness += .1
        # genome.fitness = genome.fitness / max_turns


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    try:
        winner = p.run(eval_genomes, 500)
    except KeyboardInterrupt:
        winner = p.best_genome

    # Save winner
    with open('winner.pck', 'wb') as f:
        pickle.dump(winner, f)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against itself.
    print('\nOutput:')
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    # current_contestant = random.randrange(1, 3)

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
                # original_output = max(enumerate(output), key=lambda p: p[1])[0]
                # output = [o if i in game.available_cells() else 0 for i, o in enumerate(output)]
                output = max(enumerate(output), key=lambda p: p[1])[0]
                # if original_output != output:
                #     print("(Enemy originally wanted to place on field", original_output, ")")
                if output not in game.available_cells():
                    print("Enemy fouled, you won!")
                    break
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

        if bool(input("Another turn? (0|1): ")):
            break
    # while game.available_cells():
    #     if current_contestant == 1:
    #         contestant = contestant1
    #     else:  # current_contestant == 2
    #         contestant = contestant2
    #     output = contestant.activate(game.cells_as_onehot(1))
    #     output = max(enumerate(output), key=lambda p: p[1])[0]
    #     if output not in game.available_cells():
    #         print("Contestant", current_contestant, "tried to place on already occupied field (", output, "), foul!!!")
    #         break
    #     winning_move = game.update(output, current_contestant)
    #     if winning_move:
    #         break
    #
    #     current_contestant = 1 if current_contestant == 2 else 2
    #
    #     print("\n" + game.graphical())


    node_names = {
        # -1:'#In 1:1 - 1',
        # -2:'#In 1:1 - 2',
        # -3:'#In 1:1 - 3',
        # -4:'#In 1:2 - 1',
        # -5:'#In 1:2 - 2',
        # -6:'#In 1:2 - 3',
        # -7:'#In 1:3 - 1',
        # -8:'#In 1:3 - 2',
        # -9:'#In 1:3 - 3',
        # -10:'#In 2:1 - 1',
        # -11:'#In 2:1 - 2',
        # -12:'#In 2:1 - 3',
        # -13:'#In 2:2 - 1',
        # -14:'#In 2:2 - 2',
        # -15:'#In 2:2 - 3',
        # -16:'#In 2:3 - 1',
        # -17:'#In 2:3 - 2',
        # -18:'#In 2:3 - 3',
        # -19:'#In 3:1 - 1',
        # -20:'#In 3:1 - 2',
        # -21:'#In 3:1 - 3',
        # -22:'#In 3:2 - 1',
        # -23:'#In 3:2 - 2',
        # -24:'#In 3:2 - 3',
        # -25:'#In 3:3 - 1',
        # -26:'#In 3:3 - 2',
        # -27:'#In 3:3 - 3',
        # 0: "Out 1:1",
        # 1: "Out 1:2",
        # 2: "Out 1:3",
        # 3: "Out 2:1",
        # 4: "Out 2:2",
        # 5: "Out 2:3",
        # 6: "Out 3:1",
        # 7: "Out 3:2",
        # 8: "Out 3:3"
    }
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)