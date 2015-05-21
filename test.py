import time
import math
import numpy as np
from random import choice
from game import Game

def closest(current, locs):
    return min(locs, key=lambda c: math.hypot(c[0]- current[0], c[1]-current[1]))

print(closest((1, 1), [(1, 2), (1, 3), (2, 1), (3, 3), (3, 4)]))