import random

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
print(da[0][1])
total_val = 0
for x, x_list in enumerate(da):
    val = da[x][1]
    total_val = total_val + val


weight = total_val/x
upper_limit = weight + 0.5
lower_limit = weight - 0.5

print(random.choice(da))
# # import random
# # list = [2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,8,8,8,8,8,8,9,9,9,9,9,10,10,10,10,11,11,11,12,12]
# #
# # while list != 2 :
# #     first_number = random.choice(list)
# #     list.remove(first_number)
# #     second_number = random.choice(list)
# #     list.remove(second_number)
# #     third_number = random.choice(list)
# #     list.remove(third_number)
# #     x = first_number + second_number + third_number
# #
# #     if x/3 >= 6 and x/3 <= 8:
# #         print(first_number, second_number,third_number)
# #     else:
# #         list.append(first_number)
# #         list.append(second_number)
# #         list.append(third_number)
#
# import turtle
# import time
#
# X = -300
#
#
# def draw_hexagon(board: turtle.Turtle) -> None:
#     hexagon_side = 57.735
#     board.penup()
#     board.forward(50)
#     board.pendown()
#     board.left(90)
#     board.forward(hexagon_side / 2)
#     for i in range(0, 5):
#         board.left(60)
#         board.forward(hexagon_side)
#     board.left(60)
#     board.forward(hexagon_side / 2)
#     board.penup()
#     board.left(90)
#     board.forward(50)
#     board.left(180)
#     board.pendown()
#
#
# def turtle_triangle():
#     board_length = 5  # int(input('howmuch is the board length? '))
#     board_depth = 8  # int(input('What is the board depth? '))
#
#     board = turtle.Turtle()
#     board.speed(-1)
#     board.screen.setworldcoordinates(-800, -800, 800, 800)
#     for depth in range(board_depth):
#         for length in range(board_length):
#             board.penup()
#             board.forward(100)
#
#             board.pendown()
#             draw_hexagon(board)
#             board.left(120)
#             board.forward(100)
#             board.left(120)
#             board.forward(100)
#             board.left(120)
#             board.forward(100)
#         board.penup()
#         board.sety(-((depth + 1) * 86.60))
#         if depth % 2 == 0:
#             board.setx(50)
#         else:
#             board.setx(0)
#
#     time.sleep(10000)
#
#
# def main():
#     turtle_triangle()
#
#
# if __name__ == '__main__':
#     main()
