import pygame
import random
from data_structs import Point

class Food:
    def __init__(self, surface, color, block_size, max_x, max_y):
        self.surface = surface
        self.color = color
        self.block_size = block_size
        self.max_x = max_x
        self.max_y = max_y
        self.coor = None
        self.spawn()
        self.rect = pygame.Rect(self.coor.x, self.coor.y, self.block_size, self.block_size)

    def spawn(self):
        x = random.randint(self.block_size, (self.max_x - (2 * self.block_size )) // self.block_size ) * self.block_size
        y = random.randint(self.block_size, (self.max_y - (2 * self.block_size )) // self.block_size ) * self.block_size
        self.coor = Point(x, y)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.coor.x, self.coor.y, self.block_size, self.block_size))
        
    def get_rect(self):
        return self.rect

    def get_coor(self):
        return self.coor