from pprint import pprint
import numpy as np

import board_calculator
from board_illustrator import BoardDrawing


def test_board_generation():
    calced_board = board_calculator.calculate_weights()

    tiles = [["T"] * len(p) for p in calced_board]

    board_drawing = BoardDrawing(calced_board, tiles)
    board_drawing.generate_board_outline()
    board_drawing.write_numbers()
    board_drawing.save_output()