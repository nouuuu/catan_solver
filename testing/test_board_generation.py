from pprint import pprint
import numpy as np

import board_calculator
from board_illustrator import BoardDrawing


def test_board_generation():
    calced_board = board_calculator.calculate_weights()
    tiles = board_calculator.calculate_tiles()
    board_drawing = BoardDrawing(calced_board, tiles)
    board_drawing.generate_board_outline()
    board_drawing.write_numbers()
    board_drawing.draw_harbours(board_calculator.calculate_harbours(board_drawing.tiles))
    board_drawing.save_output()

def test_calculate_harbours():
    tiles = board_calculator.calculate_tiles()
    sea_filled_tiles = BoardDrawing._fill_sea(tiles, filler='ocean')
    print()


