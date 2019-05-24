from world import World
import ai.simple

class Game:
    def __init__(self):
        self.world = World()
        self.players = (ai.simple.AI(0, self.world.grids[0]), ai.simple.AI(1, self.world.grids[1]))
        self.current_player = 0
        self.winner = None

    def tick(self):
        player = self.players[self.current_player]
        enemy = self.players[self.other_player]
        # print('tick', self.current_player, player.current_move, player.has_move)

        if not player.current_move:
            player.make_move()

        if player.current_move:
            enemy_grid = self.world.grids[self.other_player]
            x, y = player.current_move
            player.enemy_hit(x, y, enemy_grid.is_ship(x, y))
            enemy.own_hit(x, y)
            if not enemy_grid.is_ship(x, y):
                self.current_player = self.other_player
            player.end_move()

    def is_over(self):
        total_ships = sum([s[0] * s[1] for s in self.world.grids[self.current_player].SHIPS])
        discovered_ships = len(self.world.grids[self.current_player].hit_ships())
        return discovered_ships == total_ships

    @property
    def other_player(self):
        return 1 if self.current_player == 0 else 0
