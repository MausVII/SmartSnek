import torch
import random
import numpy as np
from data_structs import Point, Direction
from collections import deque

from game import Game

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        # Randomness
        self.epsilon = 0 
        # Discount rate
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.snake.direction == Direction.LEFT
        dir_r = game.snake.direction == Direction.RIGHT
        dir_u = game.snake.direction == Direction.UP
        dir_d = game.snake.direction == Direction.DOWN

        # state = [
        #     (dir_r and game.)
        # ]

    def remember(self, state, action, reward, next_state, game_over):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, game_over):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:
        old_state = agent.get_state(game)

        final_move = agent.get_action(old_state)

        reward, game_over, score = game.play_step()
        new_state = agent.get_state()

        # Train short memory on step
        agent.train_short_memory(old_state, final_move, reward, new_state, game_over)

        agent.remember(old_state, final_move, reward, new_state, game_over)

        if game_over:
            # Train long memory on whole game
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #TODO: agent.model.save()

            print(f'Game {agent.n_games}. Score {score}. Record {record}')

if __name__ == '__main__':
    train()