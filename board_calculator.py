import random
from pprint import pprint

da = [
    # how to solve the weight problem, actually use weights, not the actual numbers, 12 doesnt have a weight of 12 but 1,
    # 6 has a weight of 5, so does 8, so let the program find its numbers and calc the weight instead of the avg of the numbers
    # i think this matrix is wrong because i could just not double the numbers and use the numbers once
    # doing it this way would eliminate the need for the numbers list from the start but kills the usability if we would
    # like to change the numbers list
    # TODO: let python auto calc the weight (add up second column of da and divide by number of rows) Ulimit +0.5 Llimit -0.5 Done
    # TODO: let python get random numbers and calc with the weight of the number to see if it is a good spot
    [2, 1],
    [2, 1],
    [3, 2],
    [3, 2],
    [3, 2],
    [4, 3],
    [4, 3],
    [4, 3],
    [4, 3],
    [5, 4],
    [5, 4],
    [5, 4],
    [5, 4],
    [5, 4],
    [6, 5],
    [6, 5],
    [6, 5],
    [6, 5],
    [6, 5],
    [6, 5],
    [8, 5],
    [8, 5],
    [8, 5],
    [8, 5],
    [8, 5],
    [8, 5],
    [9, 4],
    [9, 4],
    [9, 4],
    [9, 4],
    [9, 4],
    [10, 3],
    [10, 3],
    [10, 3],
    [10, 3],
    [11, 2],
    [11, 2],
    [11, 2],
    [12, 1],
    [12, 1]
]

dm = [[(-1, 0), (-1, -1)],
      [(-1, -1), (0, -1)],
      [(0, -1), (1, -1)],
      [(1, -1), (1, 0)],
      [(1, 0), (0, 1)],
      [(0, 1), (-1, 0)]]

total_val = 0

for n, w in enumerate(da):
    weight = da[n][1]
    total_weight = total_weight + weight

avg_weight = total_val/n
UPPER_BOUND = avg_weight + 0.5
LOWER_BOUND = avg_weight - 0.5


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
                tuple_val = random.choice(da)
                val = tuple_val[1]
                try:
                    check_constraint(x, y, val, m)
                except ValueError:
                    tries += 1
                else:
                    break
            else:
                print('fail')
                return calculate_weights()
            #m[x][y] = val
            da.remove(tuple_val)
    return m

#
# calculated_m = calculate_weights()
# pprint(calculated_m)
