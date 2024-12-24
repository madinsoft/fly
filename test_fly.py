import pytest
from flyers.src.fly import Fly, WON, LOST, OK


def test_initial_state():
    fly = Fly()
    assert fly.state == OK
    assert fly.get_board() == [2, 2, 2, 2]


def test_play_valid_move():
    fly = Fly()
    fly.play(0)
    assert fly.get_board() == [3, 2, 2, 2]


def test_play_invalid_move():
    fly = Fly()
    with pytest.raises(ValueError):
        fly.play(4)


def test_contiguous_values():
    fly = Fly(board=[1, 2, 2, 2])
    fly.play(0)
    assert fly.get_board() == [0, 0, 2, 2]


def test_is_lost():
    fly = Fly(board=[5, 2, 2, 2])
    assert fly.is_lost()
    assert fly.state == LOST


def test_is_won():
    fly = Fly(board=[0, 0, 0, 0])
    assert fly.is_won()
    assert fly.state == WON


def test_game_state_ok():
    fly = Fly(board=[2, 2, 2, 2])
    assert fly.state == OK


def test_game_state_lost():
    fly = Fly(board=[5, 2, 2, 2])
    assert fly.state == LOST


def test_game_state_won():
    fly = Fly(board=[0, 0, 0, 0])
    assert fly.state == WON


def test_explore_valid_move():
    fly = Fly()
    new_board, state = fly.explore(0)
    assert new_board == [3, 2, 2, 2]
    assert state == OK


def test_explore_invalid_move():
    fly = Fly()
    with pytest.raises(ValueError):
        fly.explore(4)


def test_explore_game_over():
    fly = Fly(board=[0, 0, 0, 0])
    with pytest.raises(ValueError):
        fly.explore(0)


def test_explore_contiguous_values():
    fly = Fly(board=[1, 2, 2, 2])
    new_board, state = fly.explore(0)
    assert new_board == [0, 0, 2, 2]
    assert state == OK


def test_explore_resulting_in_lost():
    fly = Fly(board=[4, 2, 2, 2])
    new_board, state = fly.explore(0)
    assert new_board == [5, 2, 2, 2]
    assert state == LOST


def test_explore_resulting_in_won():
    fly = Fly(board=[0, 0, 0, 1])
    new_board, state = fly.explore(2)
    assert new_board == [0, 0, 0, 0]
    assert state == WON


if __name__ == "__main__":
    pytest.main()
