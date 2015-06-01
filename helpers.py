import collections, heapq, re, math

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

class PriorityQueue():
    """
    Create a priority queue for the a_star pathfinding function
    """
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Map():
    """
    Create the map that allows us to move around and look at our surroundings
    """
    def parse_tile(self, tile, loc):
        mine = re.match('\$([-0-9])', tile)
        empty_mine = re.match('\$-', tile)
        my_mine = re.match('\$1', tile)
        enemy_mine = re.match('\$([0-9])', tile)
        hero = re.match('\@([0-9])', tile)
        if(tile == '##'):
            self.walls.append(loc)
        if(tile == '[]'):
            self.taverns.append(loc)
        if(mine):
            self.all_mines.append(loc)
        if(empty_mine):
            self.empty_mines.append(loc)
        if(my_mine):
            self.my_mines.append(loc)
        if(enemy_mine):
            self.enemy_mines.append(loc)
        if(hero):
            self.heroes.append(loc)

    def parse_tiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]

        map = [[self.parse_tile(x, (si, i)) for i, x in zip(range(len(xs)), xs)] for si, xs in zip(range(len(matrix)), matrix)]
        self.weights = {loc: 5 for loc in self.heroes}

        return map

    def __init__(self, length, board):
        self.size = board['size']
        self.width = length
        self.height = length
        self.walls = []
        self.all_mines = []
        self.empty_mines = []
        self.my_mines = []
        self.enemy_mines = []
        self.heroes = []
        self.taverns = []
        self.weights = {}
        self.parse_tiles(board['tiles'])

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
    """
    Small function to help with the a_star pathfinding
    """
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph, start, goal):
    """
    The pathfinding function that allows us to find our way to things
    """
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
    """
    Since a_star returns a backwards array of where you come from, reverse the array
    """
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def draw_tile(graph, id, style, width):
    """
    draw each tile for draw_grid
    """
    r = "."
    # if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'path' in style and id in style['path']: r = "="
    if id in graph.walls: r = "#"
    if id in graph.taverns: r = "T"
    if id in graph.heroes: r = "@"
    if id in graph.empty_mines: r = "$"
    if id in graph.my_mines: r = "$1"
    if id in graph.enemy_mines: r = "$E"
    if 'goal' in style and id == style['goal']: r = "%"
    return r

def draw_grid(graph, width=2, print_statement='', **style):
    """
    Draw the visiual of the grid
    """
    for x in range(graph.width):
        for y in range(graph.height):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print(print_statement)

def closest(current, locs):
    """
    Find the closest location to current
    """
    return min(locs, key=lambda c: math.hypot(c[0] - current[0], c[1] - current[1]))

def make_helpers(game):
    """
    Make helpers for moving the charachter around
    """
    current = game.heroes[0].pos
    def move_to(place):
        """
        Automatically move the charachter to specific place
        """
        if type(place) is str:
            goal = closest(current, game.map.__dict__[place])
        else:
            goal = place

        came_from, cost_so_far = a_star(game.map, current, goal)

        path = reconstruct_path(came_from, current, goal)
        print(draw_grid(game.map, goal=goal, path=path, number=cost_so_far))

        print('Current:', current)
        print('Next Position:', path[1])

        direction = tuple(x - y for x, y in zip(path[1], path[0]))

        print('Direction Tuple:', direction)

        if direction[0] > 0: # Positive X
            return "South"
        if direction[0] < 0: # Negative X
            return "North"
        if direction[1] > 0: # Positive Y
            return "East"
        if direction[1] < 0: # Negative Y
            return "West"

        return "Stay"

    def next_to(place):
        """
        Find if charachter is next to place
        """
        if game.map.__dict__[place] == []:
            return False
        if type(place) is str:
            goal = closest(current, game.map.__dict__[place])
        else:
            goal = place
        distance = tuple(x - y for x, y in zip(goal, current))
        if distance == (1, 0):
            return True
        elif distance == (-1, 0):
            return True
        elif distance == (0, 1):
            return True
        elif distance == (0, -1):
            return True
        else:
            return False

    return move_to, next_to