import os

import pytest

from board_illustrator import BoardDrawing


def test_board_drawing():
    board = BoardDrawing([[0, 2, 3, 4], [1, 2, None, 4], [1, 2, 3, 4], [1, 2, None, 4]],
                         [["D", 'Wo', 'Wh', 'O'],
                          ['B', 'S', 'Wh', 'Wo'],
                          ['B', 'S', 'Wh', 'Wo'],
                          ['B', 'S', 'Wh', 'Wo']]
                         )
    with pytest.raises(ValueError):
        BoardDrawing([[1], [None, 4]], [['B', 'H'], [None, 'W']])

    board.generate_board_outline()
    board.write_numbers()
    board.save_output()
    assert os.path.exists(board.file_name)


def test_fill_sea():
    assert BoardDrawing._fill_sea([[1, 2], [3, 4]]) == [[None, None, None, None], [None, 1, 2, None],
                                                        [None, 3, 4, None], [None, None, None, None]]
    assert BoardDrawing._fill_sea([[1, 2], [3, 4]], "sea") == [["sea", "sea", "sea", "sea"], ["sea", 1, 2, "sea"],
                                                        ["sea", 3, 4, "sea"], ["sea", "sea", "sea", "sea"]]
