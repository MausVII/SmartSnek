from collections import namedtuple
from enum import Enum

class Direction(Enum):
    # Anti-clockwise, like degrees
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

Point = namedtuple('Point', 'x, y')