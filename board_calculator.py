import random
from copy import deepcopy
from operator import itemgetter
from pprint import pprint

import math

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
                [0, 0, 0, 0, 0, 0, 0, 0]]


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
UPPER_BOUND = avg_weight + 0.5
LOWER_BOUND = avg_weight - 0.5


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


def check_ocean_tiles(x, y, val, m, dm):
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
                local_tiles[row_index][column_index] = 'desert'
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


# even-r layout https://www.redblobgames.com/grids/hexagons/#neighbors-offset
# odd rows are long rows are 1:
# even rows are short rows are 0:


NEIGHBOUR_COORDS = {1: [(-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1)],
                    0: [(-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (1, -1), ]}

# CHECK https://imgur.com/xUzizDI for relative corner directions and calculations

NEIGHBOUR_NODES = {1: [(-1, 0, 5, 4), (-1, -1, 4, 3), (0, -1, 3, 2), (-1, 1, 0, 5), (1, 0, 2, 1), (0, 1, 1, 0)],
                   # long 1, -1 is wrong has to be -1 , 1, fix in NEIGHBOUR_COORDS
                   0: [(-1, 0, 5, 4), (0, -1, 4, 3), (1, 0, 2, 1), (1, 1, 1, 0), (0, 1, 0, 5), (1, -1, 3, 2), ]}


# 0: [(-1, 0, 4, 5), (0, -1, 5, 0), (1, 0, 1, 2), (1, 1, 2, 3), (0, 1, 3, 4), (1, -1, 0, 1), ]}


def get_neighbours(row_index, column_index, n_coords, local_tiles):
    res = []
    for c, r, node_a, node_b in n_coords:
        try:
            res.append((column_index + c, row_index + r, local_tiles[row_index + r][column_index + c], node_a, node_b))
        except IndexError:
            pass
    return res


def oddr_to_cube(col, row):
    x = col - (row - (row & 1)) / 2
    z = row
    y = -x - z
    return x, y, z


def cube_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])) / 2


def calc_distance(a, b):
    a_cube = oddr_to_cube(a[0], a[1])
    b_cube = oddr_to_cube(b[0], b[1])
    return cube_distance(a_cube, b_cube)


def calculate_harbours(local_tiles):
    harbour_list = []

    for row_index, x_list in enumerate(local_tiles):
        for column_index, val in enumerate(x_list):
            n_coords = NEIGHBOUR_NODES[row_index % 2]
            if val != 'ocean':  # this means this is a land tile
                continue
            n_tiles = get_neighbours(row_index, column_index, n_coords, local_tiles)
            land_neighbours = [t for t in n_tiles if t[2] not in ('ocean', 'harbour')]
            # print(column_index, row_index, land_neighbours)
            is_next_to_harbour = any(t for t in n_tiles if t[2] == 'harbour')
            if len(land_neighbours) > 1 and not is_next_to_harbour:
                local_tiles[row_index][column_index] = "harbour"
                harbour_list.append([column_index, row_index, land_neighbours, ""])

    tbd_harbour = harbour_list[0]
    resource_list = ['ore', 'wood', 'sheep', 'wheat', 'brick']
    harbournr = 0
    while tbd_harbour:
        # fill harbour type
        harbour_kind = '2_to_1_'
        if harbournr % 2 == 0:
            harbour_kind = '3_to_1'
        else:
            resource_list_number = int(((harbournr - 1) / 2)) % 5
            harbour_kind = harbour_kind + resource_list[resource_list_number]
        tbd_harbour[3] = harbour_kind
        harbournr += 1
        # find next closest neighbour
        tbd_harbour_distances = [(i, calc_distance(tbd_harbour, h)) for i, h in enumerate(harbour_list) if not h[3]]
        try:
            tbd_harbour = harbour_list[sorted(tbd_harbour_distances, key=itemgetter(1))[0][0]]
        except IndexError:
            break

    return harbour_list


def catan_board_to_string(local_tiles):
    return "\n".join(["".join("{0: <8}".format(s) for s in x) for x in local_tiles])


if __name__ == '__main__':
    pprint(calculate_tiles())
