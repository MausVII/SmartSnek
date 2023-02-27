import sys
sys.path.append(".")
import torch
import random
import numpy as np
from data_structs import Point, Direction
from collections import deque

from game import Game
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
# Randomness
EPSILON = 0
# Learning Rate
LR = 0.001
# Discount rate
GAMMA = 0.9
# Input network, Hidden network, Output network
NETWORK_SIZES = (11, 256, 3)

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = EPSILON
        self.gamma = GAMMA
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(*NETWORK_SIZES)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake.segments[0]
        # center_coor = Point(game.win_width // 2, game.win_height // 2)
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.snake.direction == Direction.LEFT
        dir_r = game.snake.direction == Direction.RIGHT
        dir_u = game.snake.direction == Direction.UP
        dir_d = game.snake.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.coor[0] < head.x,  # food left
            game.food.coor[0] > head.x,  # food right
            game.food.coor[1] < head.y,  # food up
            game.food.coor[1] > head.y  # food down
            ]
        # dtype=int will turn bools into ints
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        # Pop if max memory is reached
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state_zero = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_zero)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

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

        reward, game_over, score = game.play_step(final_move)
        new_state = agent.get_state(game)

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
                agent.model.save()

            print(f'Game {agent.n_games}. Score {score}. Record {record}')

if __name__ == '__main__':
    train()