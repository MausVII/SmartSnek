import pygame
from enum import Enum
from data_structs import Direction
from colors import COLORS
from snake import Snake
from food import Food

pygame.init()

SPEED = 40
WIN_HEIGHT = 720
WIN_WIDTH = 1280
INITIAL_SIZE = 3
HUMAN_SPEED = 20
BLOCK_SIZE = 20

class gameModes(Enum):
    WallCollision = 0
    WallLess = 1

class Game:
    def __init__(self, width=WIN_WIDTH, height=WIN_HEIGHT, gameMode=gameModes.WallLess):
        self.win_width = width
        self.win_height = height
        self.display = pygame.display.set_mode((self.win_width, self.win_height))
        self.clock = pygame.time.Clock()
        self.isGameRunning = True
        self.gameMode = gameMode
        self.snake = Snake(self.win_width / 2, self.win_height / 2, INITIAL_SIZE, BLOCK_SIZE, self.display)
        self.food = Food(self.display, COLORS["food"], BLOCK_SIZE, self.win_width, self.win_height)

        self.reward = 0
        self.step = 0

    def game_loop(self):
        while self.isGameRunning:
            if self.step > 100 * len(self.snake.segments):
                self.isGameRunning = False
            # Keep track of snake eating
            hasEaten = False

            self.do_input()

            self.do_collision_logic()
            
            hasEaten = self.do_food_collision()

            self.update(hasEaten)

            self.clock.tick(HUMAN_SPEED)

            self.step += 1

        pygame.quit()

    def reset(self):
        self.reward = -10
        self.snake.reset(self.win_width / 2, self.win_height / 2, INITIAL_SIZE)

    def do_collision_logic(self):
        # Wall Collision
        if self.snake.is_colliding_wall(self.win_width, 0):
            if self.gameMode == gameModes.WallLess:
                self.snake.traverse_wall(0, self.win_width)
            elif self.gameMode == gameModes.WallCollision:
                self.reset()
        if self.snake.is_colliding_wall(self.win_height, 1):
            if self.gameMode == gameModes.WallLess:
                self.snake.traverse_wall(1, self.win_height)
            elif self.gameMode == gameModes.WallCollision:
                self.reset()
        # Self Collision
        if self.snake.is_self_colliding():
            self.reset()

    def do_food_collision(self):
        if self.snake.is_colliding_with(self.food.get_coor()):
            self.food.spawn()
            if self.snake.is_colliding_with(self.food.get_coor()):
                self.food.spawn()
                self.reward = 10
            return True
        return False

    def update(self, hasEaten):
        self.display.fill(COLORS["background"])
        # Update Snake
        self.snake.update(hasEaten)
        self.snake.draw()
        # Draw Food
        self.food.draw()
        # Draw Score
        pygame.display.flip()

    def do_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and not self.snake.is_danger_lockout(self.win_width, self.win_height):
                    if event.key == pygame.K_ESCAPE:
                        self.isGameRunning = False
                    elif event.key == pygame.K_RIGHT:
                        self.snake.move(Direction.RIGHT)
                    elif event.key == pygame.K_UP:
                        self.snake.move(Direction.UP)
                    elif event.key == pygame.K_LEFT:
                        self.snake.move(Direction.LEFT)
                    elif event.key == pygame.K_DOWN:
                        self.snake.move(Direction.DOWN)

if __name__ == '__main__':
    game = Game()
    game.game_loop()