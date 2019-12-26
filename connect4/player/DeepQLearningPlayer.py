from connect4.player.Player import Player
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

class DeepQLearningPlayer(Player):
    '''
    Class for a Deep Q-Learning model
    https://www.analyticsvidhya.com/blog/2019/04/introduction-deep-q-learning-python/
    '''
    def __init__(self, num_cols=7, board_h=7, explore=True, alpha=0.1):
        super().__init__()

        if num_cols != 7 or board_h != 7:
            raise ValueError('This model only works for a 7x7 board with 4-in-a-row winning condition')

        self.is_human = False
        self.num_actions = num_cols
        self.num_cells = board_h * num_cols

        #  initialize model hyperparameters
        self.alpha = alpha if explore else 0.0
        self.gamma = 0.1  # "greediness" or "discount" factor. Higher value means more long-term strategy

        #  initialize model for approximating target function
        # Q(s, a) -> expected_reward
        # s will be represented as a single np array
        # three sequential elements of the array will be a one hot encoded representation of one cell
        #  meaning: a board 'MY' is represented as 100010, M=100, Y=010, E=001
        # I also one hot encode the 7 possible actions and tag them onto the end of the input vector
        # Thus, total length of input vector is 7 * 7 * 3 + 7
        self.num_nn_inputs = 7 * 7 * 3 + 7
        self.q_model = Sequential()
        self.q_model.add(Dense(100, input_dim=self.num_nn_inputs, activation='tanh'))
        self.q_model.add(Dense(100, activation='tanh'))
        self.q_model.add(Dense(100, activation='tanh'))
        self.q_model.add(Dense(1, activation='linear'))
        self.q_model.compile(loss='mean_squared_error', optimizer='sgd')

    def _build_input_vec(self, state, action):
        '''
        Turns a board state representation string into a one hot encoded input to the NN
        :param state: representation of current board state (string of Ms, Ys, and Es)
        :return:
        '''
        # TODO: I'm 100% certain there is a cleaner/faster way to write this method ;)
        if len(state) != self.num_cells:
            raise ValueError('state representation must have 7x7 cells!')

        ans = np.full(self.num_nn_inputs, 0)
        cur_cell = 0
        for c in state:
            if c == 'M':
                ans[cur_cell] = 1
            elif c == 'Y':
                ans[cur_cell+1] = 1
            elif c == 'E':
                ans[cur_cell + 2] = 1
            else:
                raise ValueError(f'Encountered unexpected character in state string: {c}')
            cur_cell += 3

        ans[cur_cell + action] = 1
        ans = np.reshape(ans, (1, self.num_nn_inputs))
        return ans

    def move(self, state: str) -> int:
        if np.random.uniform(0, 1) < self.alpha:
            # explore: select a random action
            action = np.random.randint(0, self.num_actions)
        else:
            # exploit: select the action with max value (future reward)
            # if multiple actions yield the same value, pick between them randomly
            action, best_reward = 0, -10000
            for i in range(self.num_actions):
                state_and_action = self._build_input_vec(state, i)
                reward = self.q_model.predict(state_and_action)
                if reward > best_reward:
                    action, best_reward = i, reward

        return action

    def train(self, history) -> None:
        '''
        Updates the q_matrix NN against the new (state,action,reward) combinations
        :param history: a list of Tuples, each tuple is a (state, action, reward)
        '''
        x = np.ndarray((len(history), self.num_nn_inputs))
        y = np.ndarray((len(history), 1))
        for ix, record in enumerate(history):
            state, action, reward = record
            nn_input = self._build_input_vec(state, action)
            x[ix] = nn_input
            y[ix] = reward

        self.q_model.fit(x, y)


if __name__ == '__main__':
    '''
    Train the model
    '''

    import os
    import fnmatch
    import pickle


    # Load most recent model OR create a new one
    candidate_models = []
    for fname in os.listdir('data'):
        if fnmatch.fnmatch(fname, 'dqn_model_*.pkl'):
            candidate_models.append(fname)

    if len(candidate_models) == 0:
        model = DeepQLearningPlayer()
    else:
        # get most recent model
        stamps = [int(cm.split('_')[2][:-4]) for cm in candidate_models]
        model_fname = f'dqn_model_{max(stamps)}.pkl'
        with open('data/'+model_fname, 'rb') as f:
            model = pickle.load(f)
    print('model loaded or created!')

    # Load most recent history dataset
    candidate_data = []
    for fname in os.listdir('data'):
        if fnmatch.fnmatch(fname, 'gamelog_*.txt'):
            candidate_data.append(fname)

    if len(candidate_data) == 0:
        raise ValueError('No training data found in ./data directory!')
    else:
        # get most recent data
        stamps = [int(cd.split('_')[1][:-4]) for cd in candidate_data]
        data_fname = f'gamelog_{max(stamps)}.txt'
        with open('data/'+data_fname, 'rb') as f:
            data = pickle.load(f)
    print(f'historical data loaded! Number of games in history is {len(data)}')

    # train model
    model.train(data)

    # save model
    import time
    ts = str(round(time.time()))
    fname = 'data/dqn_model_'+ts+'.pkl'
    with open(fname, 'wb') as f:
        pickle.dump(model, f)
