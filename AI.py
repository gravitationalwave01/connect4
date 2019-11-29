import numpy as np
from Board import Board

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

    def __init__(self, b: Board):
        '''
        alpha and gamma defined here https://en.wikipedia.org/wiki/Q-learning
        '''
        self.alpha = 0.1  # learning rate
        self.gamma = 0.1  # discount factor
        self.num_actions = b.width
        self.mat = {}
        self.last_state = None
        self.last_action = None
        self.reward = 1  # reward for winning

    def update(self, b: Board, win, illegal):
        state = str(b)
        if state not in self.mat:
            self.mat[state] = np.zeros(self.num_actions)

        reward = 0
        if win:
            reward = 1
        if illegal:
            reward = -1
            print('MADE ILLEGAL MOVE')

        self.mat[self.last_state][self.last_action] = \
            (1 - self.alpha) * self.mat[self.last_state][self.last_action] + \
            self.alpha * (reward + self.gamma * np.amax(self.mat[state]))

    def move(self, b: Board):
        state = str(b)
        if state not in self.mat:
            self.mat[state] = np.zeros(self.num_actions)

        if np.random.uniform(0, 1) < self.alpha:
            # explore: select a random action
            action = np.random.randint(0, self.num_actions)
        else:
            # exploit: select the action with max value (future reward)
            action = np.argmax(self.mat[state])

        self.last_state = state
        self.last_action = action

        return action
