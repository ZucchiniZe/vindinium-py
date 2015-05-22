import collections
import heapq
import re
import itertools

class PriorityQueue():
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Map():
    def __parse_tile(self, tile, loc):
        mine = re.match('\$([-0-9])', tile)
        hero = re.match('\@([0-9])', tile)
        if(tile == '##'):
            self.walls.append(loc)
        if(tile == '[]'):
            self.taverns.append(loc)
        if(mine):
            self.mines.append(loc)
        if(hero):
            self.heroes.append(loc)

    def __parse_tiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]

        map = [[self.__parse_tile(x, (si, i)) for i, x in zip(range(len(xs)), xs)] for si, xs in zip(range(len(matrix)), matrix)]
        self.weights = {loc: 5 for loc in self.heroes}

        return map

    def __init__(self, length, board):
        self.size = board['size']
        self.width = length
        self.height = length
        self.walls = []
        self.mines = []
        self.heroes = []
        self.taverns = []
        self.weights = {}
        self.__parse_tiles(board['tiles'])

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, a, b):
        return self.weights.get(b, 1)

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path[::-1]