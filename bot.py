from game import Game
from helpers import make_helpers

bots = ['HealthAndMineBot()']

class Bot:
    pass

class HealthAndMineBot(Bot):
    def move(self, state):
        self.game = Game(state)
        turns = self.game.turn
        hero = self.game.heroes[0]
        move_to, next_to = make_helpers(self.game)

        if hero.life > 50:
            print('Turns:', turns)
            if next_to('my_mines'):
                return move_to('enemy_mines')
            return move_to('empty_mines')
        else:
            move = move_to('taverns')
            return move_to('taverns')