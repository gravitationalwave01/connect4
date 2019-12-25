from connect4.Controller import Controller
from connect4.player.HumanPlayer import HumanPlayer

import pytest
from mock import patch

@patch('connect4.Controller.pygame', autospec=True)
@patch('connect4.Controller.Drawer', autospec=True)
def test_initialization_with_0_human_players(drawer_mock, pygame_mock):
    c = Controller(num_humans=0)
    assert not isinstance(c.player1, HumanPlayer)
    assert not isinstance(c.player2, HumanPlayer)

@patch('connect4.Controller.pygame', autospec=True)
@patch('connect4.Controller.Drawer', autospec=True)
def test_initialization_with_1_human_players(drawer_mock, pygame_mock):
    c = Controller(num_humans=1)
    assert isinstance(c.player1, HumanPlayer)
    assert not isinstance(c.player2, HumanPlayer)

@patch('connect4.Controller.pygame', autospec=True)
@patch('connect4.Controller.Drawer', autospec=True)
def test_initialization_with_2_human_players(drawer_mock, pygame_mock):
    c = Controller(num_humans=2)
    assert isinstance(c.player1, HumanPlayer)
    assert isinstance(c.player2, HumanPlayer)

@patch('connect4.Controller.pygame', autospec=True)
@patch('connect4.Controller.Drawer', autospec=True)
@pytest.mark.parametrize("num_human_players", [
    (0.1),
    (-1),
    (3),
])
def test_initialization_invalid_number_human_players_raises_exception(drawer_mock, pygame_mock, num_human_players):
    with pytest.raises(ValueError) as e:
        Controller(num_humans=num_human_players)
        assert str(num_human_players) in str(e)
