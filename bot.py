import math
import numpy as np
from collections import namedtuple
from random import choice
from game import Game
from helpers import a_star

Directions = namedtuple('Directions', 'stay up down right left')

class Bot:
    pass

class BestBot(Bot):
    def __init__(self):
        self.dirs = Directions('Stay', 'North', 'South', 'East', 'West')

    def closest(self, current, locs):
        return min(locs, key=lambda c: math.hypot(c[0] - current[0], c[1] - current[1]))

    def move_to(self, place, current):
        closest = self.closest(current, self.game.__dict__[place + "_locs"])
        if current[0] < closest[0]:
            return self.dirs.right
        elif current[0] > closest[0]:
            return self.dirs.left
        elif current[1] < closest[1]:
            return self.dirs.up
        elif current[1] > closest[1]:
            return self.dirs.down
        else:
            return self.dirs.stay

    def move(self, state):
        self.game = Game(state)
        game = self.game
        hero = game.heroes[0]
        print(hero.pos, end=' ')

        if hero.life > 50:
            print(self.closest(hero.pos, self.game.mines_locs), self.move_to('mines', hero.pos))
            return self.move_to('mines', hero.pos)

        dirs = ['Stay', 'North', 'South', 'East', 'West'] # Up Down Right Left
        # return choice(dirs)