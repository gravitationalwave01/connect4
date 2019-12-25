import pytest
from connect4.Cell import Cell
from connect4.Board import Board

@pytest.mark.parametrize("boardsize,col",[
    ((2, 2), 0),
    ((2, 2), 1),
    ((1, 1), 0)
])
def test_find_top_empty_board(boardsize, col):
    b = Board(*boardsize)
    row = b.find_top(col)
    expected = b.height - 1
    assert row == expected

@pytest.mark.parametrize("board_size,up_to",[
    ((2, 2), 0),
    ((2, 2), 1)
])
def test_find_top_with_col_filled(board_size, up_to):
    b = Board(*board_size)
    for i in range(up_to):
        row_to_populate = b.height - i - 1
        b.cells[0, row_to_populate] = Cell.BLACK

    row = b.find_top(0)
    expected = b.height - up_to - 1
    assert row == expected

@pytest.mark.parametrize("board_size,num_moves",[
    ((2, 2), 0),
    ((2, 2), 1)
])
def test_move_one_square(board_size, num_moves):
    b = Board(*board_size)
    for i in range(num_moves):
        row = b.move(0, Cell.BLACK)
        expected_row = b.height - i - 1
        assert row == expected_row
        assert b.cells[0, expected_row] == Cell.BLACK

def test_move_too_tall_move_raises_exception():
    b = Board(2, 2)
    b.move(0, Cell.BLACK)
    b.move(0, Cell.BLACK)
    with pytest.raises(ValueError) as excinfo:
        b.move(0, Cell.BLACK)

    assert 'Illegal move' in str(excinfo.value)

def test_move_too_wide_move_raises_exception():
    b = Board(2, 2)
    with pytest.raises(ValueError) as excinfo:
        b.move(2, Cell.BLACK)

    assert 'Illegal move' in str(excinfo.value)

@pytest.mark.parametrize("arr,color,num,expected",[
    (['R', 'R', 'B'], 'R', 2, True),
    (['B', 'R', 'B'], 'R', 2, False),
    (['B', 'R', 'B'], 'B', 2, False),
    (['B', 'R', 'B'], 'R', 1, True),
    (['B', 'B', 'B'], 'B', 3, True),
    (['W', 'R', 'B'], 'R', 2, False),
])
def test_check_for_n_in_row(arr, color, num, expected):
    b = Board(2, 2, num)
    res = b.check_for_connect(arr, color)
    assert res == expected

def test_check_winning_move_main_diagonal_win():
    b = Board(2, 2, 2)
    b.cells[1, 0] = Cell.BLACK
    b.cells[0, 1] = Cell.BLACK
    assert b.check_winning_move(1, 0)
    assert b.check_winning_move(0, 1)

def test_check_winning_move_second_diagonal_win():
    b = Board(2, 2, 2)
    b.cells[0, 0] = Cell.BLACK
    b.cells[1, 1] = Cell.BLACK
    assert b.check_winning_move(1, 1)
    assert b.check_winning_move(0, 0)

def test_check_winning_off_second_diagonal_win():
    b = Board(3, 3, 2)
    b.cells[1, 0] = Cell.BLACK
    b.cells[2, 1] = Cell.BLACK
    assert b.check_winning_move(1, 0)
    assert b.check_winning_move(2, 1)

def test_check_winning_off_main_diagonal_win():
    b = Board(3, 3, 2)
    b.cells[0, 1] = Cell.BLACK
    b.cells[1, 2] = Cell.BLACK
    assert b.check_winning_move(0, 1)
    assert b.check_winning_move(1, 2)


def test_string_representation_complex_case():
    b = Board(2, 2, 2)
    b.move(0, Cell.BLACK)
    b.move(1, Cell.RED)
    b.move(0, Cell.BLACK)
    b_str = str(b)
    expected = str(Cell.BLACK.value) + str(Cell.BLACK.value) + str(Cell.EMPTY.value) + str(Cell.RED.value)
    assert b_str == expected
