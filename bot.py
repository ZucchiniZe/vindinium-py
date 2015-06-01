import json, logging
from helpers import Game, make_helpers

bots = ['HealthAndMineBot()']

class Bot:
    pass

class HealthAndMineBot(Bot):
    def move(self, state):
        json_state = json.dumps(state, indent=2)
        self.game = Game(state)
        turns = self.game.turn
        hero = self.game.heroes[0]
        move_to, next_to, closest, distance = make_helpers(self.game)

        if hero.life > 50:
            logging.warning('Turns: {0}'.format(turns))
            logging.warning('Closest {0}: {1}'.format('Heroes', closest('heroes')))
            if next_to('my_mines'):
                return move_to('enemy_mines')
            return move_to('empty_mines')
        else:
            return move_to('taverns')