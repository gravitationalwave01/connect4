import numpy as np
from Board import Board
from Environment import Environment
import pickle

class DummyAI(object):
    '''
    Contains logic for a very dumb AI
    '''
    def __init__(self):
        pass

    def update(self):
        pass

    @staticmethod
    def move(b: Board):
        return np.random.randint(0, b.width)


class QLearningAI(object):

    def __init__(self, env: Environment, explore=True):
        '''
        alpha and gamma defined here https://en.wikipedia.org/wiki/Q-learning
        '''
        self.alpha = 0.1 if explore else 0.0
        self.gamma = 0.1  # "greediness" or "discount" factor
        self.num_actions = env.num_actions
        self.mat = {}
        self.env = env

    def update(self, reward, state, action, new_state):
        if new_state not in self.mat:
            self.mat[new_state] = np.zeros(self.num_actions)

        self.mat[state][action] = \
            (1 - self.alpha) * self.mat[state][action] + \
            self.alpha * (reward - self.gamma * np.amax(self.mat[new_state]))

    def move(self):
        state = self.env.get_state()
        if state not in self.mat:
            self.mat[state] = np.zeros(self.num_actions)

        if np.random.uniform(0, 1) < self.alpha:
            # explore: select a random action
            action = np.random.randint(0, self.num_actions)
        else:
            # exploit: select the action with max value (future reward)
            max_score = np.amax(self.mat[state])
            where = np.where(self.mat[state] == max_score)
            action = np.random.choice(where[0])  # np.where returns a tuple...

        reward = self.env.take_action(action)
        new_state = self.env.get_state()
        self.update(reward, state, action, new_state)

    def save(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump(self.mat, f)

    def load(self, fname):
        with open(fname, 'rb') as f:
            self.mat = pickle.load(f)
