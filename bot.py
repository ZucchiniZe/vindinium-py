from game import Game
from helpers import a_star, reconstruct_path, draw_grid, make_move_to

bots = ['HealthAndMineBot']

class Bot:
    pass

class HealthAndMineBot(Bot):
    def move(self, state):
        self.game = Game(state)
        hero = self.game.heroes[0]
        move_to = make_move_to(self.game)

        if hero.life > 50:
            move = move_to('mines', hero.pos)
            print('Direction:', move)
            return move
        else:
            move = move_to('taverns', hero.pos)
            print('Direction:', move)
            return move