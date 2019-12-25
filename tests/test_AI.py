from AI import QLearningAI
from Environment import Environment
from mock import patch
import numpy as np

@patch('Environment.Environment.get_state', return_value='123')
@patch('numpy.random.uniform', return_value=0.0)
def test_update_new_state_added_correctly(uniform_mock, get_state_mock):
    env = Environment(board_w=2, board_h=2, num_to_win=2)
    ai = QLearningAI(env)
    ai.move()
    assert '123' in ai.mat.keys()

@patch('Environment.Environment.get_state', return_value='123')
@patch('Environment.Environment.take_action', return_value=0)
@patch('numpy.random.uniform', return_value=1.0)
def test_update_exploit_mode_picks_max_value(uniform_mock, take_action_mock, get_state_mock):
    env = Environment(board_w=3, board_h=3, num_to_win=3)
    ai = QLearningAI(env)
    ai.mat['123'] = np.asarray([-1, 1, 2])
    ai.move()
    take_action_mock.assert_called_once_with(2)

@patch('Environment.Environment.get_state', return_value='123')
@patch('Environment.Environment.take_action', return_value=0)
@patch('numpy.random.uniform', return_value=0.0)
@patch('numpy.random.randint', return_value=1)
def test_update_explore_mode_doesnt_pick_max_value(randint_mock, uniform_mock, take_action_mock, get_state_mock):
    env = Environment(board_w=3, board_h=3, num_to_win=3)
    ai = QLearningAI(env)
    ai.mat['123'] = np.asarray([-1, 1, 2])
    ai.move()
    take_action_mock.assert_called_once_with(1)
