import re
from helpers import Map, PriorityQueue

class Game:
    def __init__(self, state):
        self.state = state
        self.map = Map(state['game']['board']['size'], state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]
        self.turn = state['game']['turn']

class Hero:
    def __init__(self, hero):
        self.name = hero['name']
        self.pos = (hero['pos']['x'], hero['pos']['y'])
        self.life = hero['life']
        self.gold = hero['gold']