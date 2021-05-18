import pygame
from data_structs import Point, Direction
from colors import COLORS

STARTING_DIRECTION = Direction.RIGHT

class Snake:
    def __init__(self, x_start, y_start, size, block_size, display):
        self.head = Point(x_start, y_start)
        self.n_segments = size
        self.display = display
        self.block_size = block_size
        self.direction = STARTING_DIRECTION
        self.segments = list()
        self.init_body()

    def init_body(self):
        for i in range(0, self.n_segments):
            new_seg = Point(self.head.x - (i * self.block_size), self.head.y)
            self.segments.append(new_seg)

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(self.display, COLORS["snake"], pygame.Rect(segment.x, segment.y, self.block_size, self.block_size))

    def update(self, hasEaten):
        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += self.block_size
        elif self.direction == Direction.UP:
            y -= self.block_size
        elif self.direction == Direction.LEFT:
            x -= self.block_size
        elif self.direction == Direction.DOWN:
            y += self.block_size

        self.head = Point(x, y)

        self.segments.insert(0, Point(self.head.x, self.head.y))
        # Keep the last segment if it has eaten, cut it otherwise
        if not hasEaten:
            self.segments.pop()
        else:
            self.n_segments += 1

    def move(self, direction):
            if direction == Direction.RIGHT and self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
            elif direction == Direction.UP and self.direction != Direction.DOWN:
                self.direction = Direction.UP
            elif direction == Direction.LEFT and self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
            elif direction == Direction.DOWN and self.direction != Direction.UP:
                self.direction = Direction.DOWN

    def is_colliding_wall(self, line, axis):
        # Axis = 0 -> horizontal, axis = 1 -> Vertical
        if axis == 0:
            if self.head.x == line and line != 0 and self.direction == Direction.RIGHT:
                return True
            elif self.head.x == 0 and self.direction == Direction.LEFT:
                return True
            else:
                return False
        elif axis == 1:
            if self.head.y == line and line != 0 and self.direction == Direction.DOWN:
                return True
            elif self.head.y == 0 and self.direction == Direction.UP:
                return True
            else: 
                return False
        else:
            print("Wrong axis number")

    def is_self_colliding(self):
        rect_head = pygame.Rect((self.head.x, self.head.y), (self.block_size, self.block_size))
        for seg in range(1, self.n_segments):
            rect_segment = pygame.Rect((self.segments[seg].x, self.segments[seg].y), (self.block_size, self.block_size))
            if rect_head.colliderect(rect_segment):
                print("true")
                return True
        return False

    def is_colliding_with(self, food_coor):
        for seg in range(0, self.n_segments):
            if self.get_coor() == food_coor:
                return True
        return False

    def reset(self, x_start, y_start, size):
        self.head = Point(x_start, y_start)
        self.direction = STARTING_DIRECTION
        self.n_segments = size
        self.segments = []
        for i in range(0, self.n_segments):
            new_seg = Point(self.head.x - (i * self.block_size), self.head.y)
            self.segments.append(new_seg)

    def get_coor(self):
        return self.head

    def traverse_wall(self, axis, distance):
        if axis == 0:
            if self.head.x == 0:
                self.head = Point(self.head.x + distance, self.head.y)
            else:
                self.head = Point(0 - self.block_size, self.head.y)
        else:
            if self.head.y == 0:
                self.head = Point(self.head.x, self.head.y + distance)
            else:
                self.head = Point(self.head.x, 0 - self.block_size)

    # Used for wall less mode to avoid steering after traversing
    def is_danger_lockout(self, win_width, win_height):
        if self.head.x == 0 or self.head.x == win_width or self.head.y == 0 or self.head.y == win_height:
            return True
        else:
            return False
