import re
from helpers import Map, PriorityQueue

TAVERN = 0
AIR = -1
WALL = -2

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

AIM = {'North': (-1, 0),
       'East': (0, 1),
       'South': (1, 0),
       'West': (0, -1)}

class HeroTile:
    def __init__(self, id):
        self.id = id

class MineTile:
    def __init__(self, heroId = None):
        self.heroId = heroId

class Game:
    def __init__(self, state):
        self.state = state
        self.map = Map(state['game']['board']['size'], state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]

class Hero:
    def __init__(self, hero):
        self.name = hero['name']
        self.pos = (hero['pos']['x'], hero['pos']['y'])
        self.life = hero['life']
        self.gold = hero['gold']

    def __str__(self):
        return self.name