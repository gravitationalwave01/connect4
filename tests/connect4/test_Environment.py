from connect4.Environment import Environment
from connect4.Cell import Cell
import pytest

def test_get_state_black_replaced_with_M():
    '''
    The position
    B E
    B R
    should be represented as
    Y E
    Y M
    when playing as red (M=mine, Y=yours)
    '''

    env = Environment(2, 2, 2)
    env.cur_player = Cell.BLACK
    env.take_action(0)  # black moves
    env.take_action(1)  # red moves
    env.take_action(0)  # black moves
    result = env.get_state()
    expected = 'YYEM'  # what red sees
    assert result == expected

def test_get_state_red_replaced_with_M():
    '''
    The position
    R E
    R B
    should be represented as
    Y E
    Y M
    when playing as black (M=mine, Y=yours)
    '''
    env = Environment(2, 2, 2)
    env.cur_player = Cell.RED
    env.take_action(0)  # red moves
    env.take_action(1)  # black moves
    env.take_action(0)  # red moves
    result = env.get_state()
    expected = 'YYEM'  # what black sees
    assert result == expected

def test_take_action_invalid_move_returns_neg_1():
    env = Environment(2, 2, 2)
    env.cur_player = Cell.BLACK
    env.take_action(0)  # black moves
    env.take_action(1)  # red moves
    env.take_action(0)  # black moves
    result = env.take_action(0)  # Invalid move
    assert result == -1

def test_take_action_curplayer_BLACK_changes_to_RED():
    env = Environment(2, 2, 2)
    env.cur_player = Cell.BLACK
    env.take_action(0)
    assert env.cur_player == Cell.RED

def test_take_action_curplayer_RED_changes_to_BLACK():
    env = Environment(2, 2, 2)
    env.cur_player = Cell.RED
    env.take_action(0)
    assert env.cur_player == Cell.BLACK

def test_take_action_game_over_when_board_full():
    env = Environment(2, 2, 2)
    env.take_action(0)
    env.take_action(0)
    env.take_action(1)
    env.take_action(1)
    # 2x2 board is now full
    assert env.is_game_over

def test_take_action_returns_0_when_no_win():
    env = Environment(2, 2, 2)
    result = env.take_action(0)
    assert result == 0

    result = env.take_action(1)
    assert result == 0

def test_take_action_returns_1_when_win():
    env = Environment(2, 2, 2)
    env.take_action(0)  # black moves
    env.take_action(1)  # red moves
    result = env.take_action(0)  # black moves and wins
    assert result == 1

def test_reset_new_board():
    env = Environment(2, 2, 2)
    env.take_action(0)
    env.reset()
    assert env.b.cells[0, 0] == Cell.EMPTY
    assert env.b.cells[0, 1] == Cell.EMPTY
    assert env.b.cells[1, 0] == Cell.EMPTY
    assert env.b.cells[1, 1] == Cell.EMPTY

def test_reset_new_board_num_moves_reset():
    env = Environment(2, 2, 2)
    env.take_action(0)
    env.reset()
    assert env.num_moves == 0

def test_reset_history_cleared():
    env = Environment(2, 2, 2)
    env.take_action(0)
    env.reset()
    assert env.history == []

@pytest.mark.parametrize("board_w,board_h",[
    (2, 2),
    (2, 3),
    (1, 3),
    (3, 1),
])
def test_num_cells_computed_correctly(board_w, board_h):
    env = Environment(board_w, board_h, 2)
    assert env.get_num_cells() == board_w * board_h


def test_history_has_same_number_elements_as_moves():
    env = Environment(2, 2, 2)
    env.take_action(0)
    assert len(env.history) == 1

    env.take_action(0)
    assert len(env.history) == 2


def test_history_correctly_represents_history_after_one_move():
    env = Environment(2, 2, 2)
    action = 0
    start_state = env.get_state()
    reward = env.take_action(action)

    assert env.history == [(start_state, action, reward)]


def test_history_correctly_represents_history_after_several_moves():
    env = Environment(2, 2, 2)

    # make some moves
    env.take_action(0)
    env.take_action(1)

    # make one more move
    action = 0
    most_recent_state = env.get_state()
    reward = env.take_action(action)

    # check that history correctly appended to
    last_move = env.history[-1]
    assert last_move == (most_recent_state, action, reward)

