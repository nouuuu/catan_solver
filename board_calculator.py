import random
from pprint import pprint

LOWER_BOUND = 6
UPPER_BOUND = 8

dm = [[(-1, 0), (-1, -1)],
      [(-1, -1), (0, -1)],
      [(0, -1), (1, -1)],
      [(1, -1), (1, 0)],
      [(1, 0), (0, 1)],
      [(0, 1), (-1, 0)]]


def check_constraint(x, y, val, m):
    for (dx1, dy1), (dx2, dy2) in dm:
        try:
            dm1 = m[x + dx1][y + dy1]
            dm2 = m[x + dx2][y + dy2]
        except IndexError:
            continue
        if not (val and dm1 and dm2):
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
    weights_list = [2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 11,
                    11, 11, 12, 12]
    for x, x_list in enumerate(m):
        for y, val in enumerate(x_list):
            if val is None:
                continue
            tries = 0
            while tries < 100:
                val = random.choice(weights_list)
                try:
                    check_constraint(x, y, val, m)
                except ValueError:
                    tries += 1
                else:
                    break
            else:
                print('fail')
                return calculate_weights()
            m[x][y] = val
            weights_list.remove(val)
    return m

#
# calculated_m = calculate_weights()
# pprint(calculated_m)
