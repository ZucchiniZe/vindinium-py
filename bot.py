import math
import numpy as np
from collections import namedtuple
from random import choice
from game import Game
from helpers import a_star, reconstruct_path

Directions = namedtuple('Directions', 'stay up down right left')

def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'path' in style and id in style['path']: r = "="
    if id in graph.walls: r = "#"
    if id in graph.taverns: r = "T"
    if id in graph.heroes: r = "@"
    if id in graph.mines: r = "$"
    if 'goal' in style and id == style['goal']: r = "%"
    return r

def draw_grid(graph, width=2, print_statement='', **style):
    for x in range(graph.width):
        for y in range(graph.height):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print(print_statement)

class Bot:
    pass

class BestBot(Bot):
    def __init__(self):
        self.dirs = Directions('Stay', 'North', 'South', 'East', 'West')

    def goal(self, current, locs):
        return min(locs, key=lambda c: math.hypot(c[0] - current[0], c[1] - current[1]))

    def move_to(self, place, current):
        goal = self.goal(current, self.game.map.__dict__[place])
        came_from, cost_so_far = a_star(self.game.map, current, goal)
        path = reconstruct_path(came_from, current, goal)
        print(draw_grid(self.game.map, goal=goal, path=path, number=cost_so_far))
        next_pos = path[1]
        print('Current:', current)
        print('Next Position:', next_pos)
        direction = tuple(x - y for x, y in zip(path[1], path[0]))
        print('Direction Tuple:', direction)

        if direction[0] > 0: # Positive X
            return self.dirs.left
        if direction[0] < 0: # Negative X
            return self.dirs.right
        if direction[1] > 0: # Positive Y
            return self.dirs.down
        if direction[1] < 0: # Negative Y
            return self.dirs.up

        return self.dirs.stay

    def move(self, state):
        self.game = Game(state)
        game = self.game
        hero = game.heroes[0]
        # print(draw_grid(game.map))

        if hero.life > 50:
            move = self.move_to('taverns', hero.pos)
            print('Direction:', move)
            return move

        dirs = ['Stay', 'North', 'South', 'East', 'West'] # Up Down Right Left
        return choice(dirs)