import random
from copy import deepcopy
from pprint import pprint

number_cards = [
    (2, 1, 'Zb'),
    (2, 1, 'A'),
    (3, 2, 'Za'),
    (3, 2, 'L'),
    (3, 2, 'E'),
    (4, 3, 'N'),
    (4, 3, 'U'),
    (4, 3, 'C'),
    (4, 3, 'C'),
    (5, 4, 'T'),
    (5, 4, 'B'),
    (5, 4, 'W'),
    (5, 4, 'W'),
    # (5, 4, ''),
    # (6, 5, ''),
    # (6, 5, ''),
    (6, 5, 'D'),
    (6, 5, 'K'),
    (6, 5, 'C'),
    (6, 5, 'Zc'),
    (8, 5, 'M'),
    (8, 5, 'O'),
    (8, 5, 'O'),
    (8, 5, 'G'),
    # (8, 5, ''),
    # (8, 5, ''),
    (9, 4, 'X'),
    (9, 4, 'F'),
    (9, 4, 'V'),
    # (9, 4, ''),
    # (9, 4, ''),
    (10, 3, 'J'),
    (10, 3, 'P'),
    (10, 3, 'J'),
    (10, 3, 'S'),
    (11, 2, 'H'),
    (11, 2, 'I'),
    (11, 2, 'H'),
    (11, 2, 'R'),
    (11, 2, 'Q'),
    (12, 1, 'R'),
    (12, 1, 'Y')]

available_tiles = ['wood'] * 7 \
                  + ['ore'] * 7 \
                  + ['brick'] * 7 \
                  + ['wheat'] * 7 \
                  + ['sheep'] * 7 \
                  + ['desert'] * 0 \
                  + ['ocean'] * 0

board_layout = [[0, 0, 0, 0, 0, 0, 0, 0],  # x 0
                [None, 0, 0, 0, 0, None, 0, 0],  # x 1
                [0, 0, None, 0, 0, 0, 0, 0],  # x 2
                [None, 0, 0, 0, 0, None, 0, 0],  # x 3
                [0, 0, 0, 0, 0, 0, 0, 0]]  # x 4

dm_short_row = [[(-1, 0), (-1, -1)],
                [(-1, -1), (0, -1)],
                [(0, -1), (1, -1)],
                [(1, -1), (1, 0)],
                [(1, 0), (0, 1)],
                [(0, 1), (-1, 0)]]

dm_long_row = [[(-1, 0), (0, -1)],
               [(0, -1), (1, 0)],
               [(1, 0), (1, 1)],
               [(1, 1), (0, 1)],
               [(0, 1), (-1, 1)],
               [(-1, 1), (-1, 0)]]

avg_weight = sum([w[1] for w in number_cards]) / len(number_cards)
UPPER_BOUND = avg_weight + 0.25
LOWER_BOUND = avg_weight - 1


def check_constraint_weight(x, y, val, m, dm):
    for (dx1, dy1), (dx2, dy2) in dm:
        try:
            _, dm1, _ = m[x + dx1][y + dy1]  # _ means this value exists but ignore it
            _, dm2, _ = m[x + dx2][y + dy2]
        except (IndexError, TypeError):  # IndexError: don't check if a value doesn't exist,
            # TypeError is to ignore the 0's in the matrix because there isn't a tuple there yet
            continue
        if not (val):  # this is to ignore the check if there is a 0 in val, then it just fills in a number
            continue
        avg = (val + dm1 + dm2) / 3
        if not LOWER_BOUND <= avg <= UPPER_BOUND:
            raise ValueError

def check_constraint_tiles(x, y, val, m, dm):
    for (dx1, dy1), (dx2, dy2) in dm:
        try:
            dm1 = m[x + dx1][y + dy1]  # _ means this value exists but ignore it
            dm2 = m[x + dx2][y + dy2]
        except (IndexError, TypeError):  # IndexError: don't check if a value doesn't exist,
            # TypeError is to ignore the 0's in the matrix because there isn't a tuple there yet
            continue
        if not val:  # this is to ignore the check if there is a 0 in val, then it just fills in a number
            continue
        if val == dm1 or val == dm2:
            raise ValueError


def calculate_weights():
    local_board_values = deepcopy(board_layout)
    local_number_cards = deepcopy(number_cards)
    # go through rows from top to bottom, x_list is the whole row with data
    for row_index, x_list in enumerate(local_board_values):
        for column_index, val in enumerate(x_list):  # loop columns from left to right, val is the value of the cell
            row_dm = row_index % 2 != 0 and dm_short_row or dm_long_row  # select correct dm for even/odd rows
            if val is None:
                continue
            tries = 0
            while tries < 1000:
                num, val, letter = random.choice(local_number_cards)
                try:
                    check_constraint_weight(row_index, column_index, val, local_board_values, row_dm)
                except ValueError:  # thrown if the check_constraints fails, then a new random value is tried
                    tries += 1
                else:  # if try succeeds break the outer while loop and continue to setting value
                    break
            else:  # if the loop has run over its max tries the board is unsolvable and we retry with a clean board
                print('fail')
                return calculate_weights()
            local_board_values[row_index][column_index] = [num, val, letter]  # fill in the value in the final matrix
            local_number_cards.remove((num, val, letter))  # delete the value from the local_number_cards matrix
    return local_board_values


def calculate_tiles():
    local_tiles = deepcopy(board_layout)
    local_available_tiles = deepcopy(available_tiles)

    for row_index, x_list in enumerate(local_tiles):
        for column_index, val in enumerate(x_list):  # loop columns from left to right, val is the value of the cell
            row_dm = row_index % 2 != 0 and dm_short_row or dm_long_row  # select correct dm for even/odd rows
            if val is None:
                continue
            tries = 0
            while tries < 1000:
                val = random.choice(local_available_tiles)
                try:
                    check_constraint_tiles(row_index, column_index, val, local_tiles, row_dm)
                except ValueError:  # thrown if the check_constraints fails, then a new random value is tried
                    tries += 1
                else:  # if try succeeds break the outer while loop and continue to setting value
                    break
            else:  # if the loop has run over its max tries the board is unsolvable and we retry with a clean board
                return calculate_tiles()
            local_tiles[row_index][column_index] = val  # fill in the value in the final matrix
            local_available_tiles.remove(val)  # delete the value from the local_number_cards matrix
    return local_tiles

if __name__ =='__main__':
    pprint(calculate_tiles())