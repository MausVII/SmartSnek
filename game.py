import pygame
import numpy as np
from enum import Enum
from data_structs import Direction
from colors import COLORS
from snake import Snake
from food import Food

pygame.init()

SPEED = 40
WIN_HEIGHT = 480
WIN_WIDTH = 720
INITIAL_SIZE = 3
HUMAN_SPEED = 20
AI_SPEED = 40
BLOCK_SIZE = 20
TEXT_CENTER_COOR = (50, 50)
LINE_HEIGHT = 20

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
        self.score = 0
        self.record = 0

        # AI variables
        self.reward = 0
        self.step = 0
    
    def play_step(self, action):
        # food_arr = np.array([self.food.coor.x, self.food.coor.y])
        # snake_arr = np.array([self.snake.head.x, self.snake.head.y], dtype=int)
        # distance_food_bef = np.linalg.norm(food_arr - snake_arr)

        self.step += 1
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        self.move_snake(action)

        if self.is_collision() or self.step > (100 * len(self.snake.segments)):
            game_over = True
            self.reward = -10
            return self.reward, game_over, self.score
        
        hasEaten = self.do_food_collision()
        if hasEaten:
            self.reward = 20
            self.score += 1

        self.update(hasEaten)
        self.clock.tick(AI_SPEED)

        # food_arr = np.array([self.food.coor.x, self.food.coor.y])
        # distance_food_aft = np.linalg.norm(food_arr - snake_arr)

        # if distance_food_aft < distance_food_bef:
        #     self.reward = 1

        return self.reward, False, self.score

    def game_loop(self):
        while self.isGameRunning:
            # Keep track of snake eating
            hasEaten = False
            
            self.do_input()

            self.do_collision_logic()
            
            hasEaten = self.do_food_collision()

            self.update(hasEaten)

            self.clock.tick(HUMAN_SPEED)

        pygame.quit()

    """Used by neural network to control snake movement"""
    def move_snake(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.snake.direction)

        if np.array_equal(action, [1, 0, 0]):
            # Keep straight
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            # Turn right
            next_idx = (idx + 1) % len(clock_wise)
            new_dir = clock_wise[next_idx]
        else:
            # Turn left
            next_idx = (idx - 1) % len(clock_wise)
            new_dir = clock_wise[next_idx]

        self.snake.direction = new_dir

    def reset(self):
        self.reward = -10
        self.record = max(self.score, self.record)
        self.score = 0
        self.step = 0
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
            return True
        
        return False

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake.head
        # hits boundary
        if pt.x > self.win_width - BLOCK_SIZE or pt.x < 0 or pt.y > self.win_height - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake.segments[1:]:
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
        self.display_info()

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

    def display_info(self):
        # print(pygame.font.get_fonts())
        font = pygame.font.Font('./misc/fonts/Helvetica-Neue.otf', 18)
        text = [
            font.render(F'Score: {self.score}', True, COLORS['text']), 
            font.render(F'Record: {self.record}', True, COLORS['text']),
            ]
        text_rect = text[0].get_rect()
        text_rect.center = TEXT_CENTER_COOR
        for idx, line in enumerate(text):
            self.display.blit(line, (text_rect[0], text_rect[1] + (idx * LINE_HEIGHT)))


if __name__ == '__main__':
    game = Game()
    game.game_loop()