import random
from copy import deepcopy

number_cards = [
    (2, 1, 'B'),
    (2, 1, ''),
    (3, 2, ''),
    (3, 2, 'Q'),
    (3, 2, 'D'),
    (4, 3, ''),
    (4, 3, ''),
    (4, 3, 'N'),
    (4, 3, 'J'),
    (5, 4, ''),
    (5, 4, ''),
    (5, 4, ''),
    (5, 4, 'A'),
    (5, 4, 'O'),
    (6, 5, ''),
    (6, 5, ''),
    (6, 5, 'M'),
    (6, 5, 'C'),
    (6, 5, 'P'),
    (6, 5, 'E'),
    (8, 5, ''),
    (8, 5, 'K'),
    (8, 5, ''),
    (8, 5, ''),
    (8, 5, ''),
    (8, 5, ''),
    (9, 4, ''),
    (9, 4, ''),
    (9, 4, ''),
    (9, 4, ''),
    (9, 4, 'G'),
    (10, 3, 'F'),
    (10, 3, 'L'),
    (10, 3, ''),
    (10, 3, ''),
    (11, 2, 'I'),
    (11, 2, 'R'),
    (11, 2, ''),
    (12, 1, 'H'),
    (12, 1, '')]

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


def check_constraint(x, y, val, m, dm):
    for (dx1, dy1), (dx2, dy2) in dm:
        try:
            _, dm1, _ = m[x + dx1][y + dy1]  # _ means this value exists but ignore it
            _, dm2, _ = m[x + dx2][y + dy2]
        except (IndexError,
                TypeError):  # indexerror this is for ignoring the sides and top of the board with the dm-matrixs, TypeError is to ignore the 0's in the matrix because there isnt a tuple there yet
            continue
        if not (val):  # this is to ignore the check if there is a 0 in val, then it just fills in a number
            continue
        avg = (val + dm1 + dm2) / 3
        if not LOWER_BOUND <= avg <= UPPER_BOUND:
            raise ValueError


def calculate_weights():
    m = [[0, 0, 0, 0, 0, 0, 0, 0],  # x 0
         [None, 0, 0, 0, 0, None, 0, 0],  # x 1
         [0, 0, None, 0, 0, 0, 0, 0],  # x 2
         [None, 0, 0, 0, 0, None, 0, 0],  # x 3
         [0, 0, 0, 0, 0, 0, 0, 0]]
    local_number_cards = deepcopy(number_cards)
    for row_index, x_list in enumerate(
            m):  # go through rows from top to bottom row_index is the index of the row, x_list is the whole row with data
        for column_index, val in enumerate(
                x_list):  # go trough columns from left to right column_index is the index of the column, val is the value of the cell
            row_dm = row_index % 2 != 0 and dm_short_row or dm_long_row  # shorthand if statement with check for even/odd rows
            if val is None:
                continue
            tries = 0
            while tries < 1000:
                num, val, letter = random.choice(local_number_cards)
                try:
                    check_constraint(row_index, column_index, val, m, row_dm)
                except ValueError:  # this ValueError is if the check_constraints fails, then he picks a new random number from the list
                    tries += 1
                else:  # if try succeeds break this cycle and continue to setting value
                    break
            else:  # if the loop has run over its max trys the board is unsolvable and it will start from an empty matrix again with new values
                print('fail')
                return calculate_weights()
            m[row_index][column_index] = [num, val, letter]  # fill in the value in the final matrix
            local_number_cards.remove((num, val, letter))  # delete the value from the local_number_cards matrix
    return m
