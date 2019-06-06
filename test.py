# import random
# list = [2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,8,8,8,8,8,8,9,9,9,9,9,10,10,10,10,11,11,11,12,12]
#
# while list != 2 :
#     first_number = random.choice(list)
#     list.remove(first_number)
#     second_number = random.choice(list)
#     list.remove(second_number)
#     third_number = random.choice(list)
#     list.remove(third_number)
#     x = first_number + second_number + third_number
#
#     if x/3 >= 6 and x/3 <= 8:
#         print(first_number, second_number,third_number)
#     else:
#         list.append(first_number)
#         list.append(second_number)
#         list.append(third_number)

import turtle
import time

X = -300


def draw_hexagon(board: turtle.Turtle) -> None:
    hexagon_side = 57.735
    board.penup()
    board.forward(50)
    board.pendown()
    board.left(90)
    board.forward(hexagon_side/2)
    for i in range(0,5):
        board.left(60)
        board.forward(hexagon_side)
    board.left(60)
    board.forward(hexagon_side/2)
    board.penup()
    board.left(90)
    board.forward(50)
    board.left(180)
    board.pendown()

def turtle_triangle():
    board_length = 5#int(input('howmuch is the board length? '))
    board_depth = 8#int(input('What is the board depth? '))

    board = turtle.Turtle()
    board.speed(-1)
    board.screen.setworldcoordinates(-800,-800,800,800)
    for depth in range(board_depth):
        for length in range(board_length):
            board.penup()
            board.forward(100)

            board.pendown()
            draw_hexagon(board)
            board.left(120)
            board.forward(100)
            board.left(120)
            board.forward(100)
            board.left(120)
            board.forward(100)
        board.penup()
        board.sety(-((depth + 1) * 86.60))
        if depth % 2 == 0:
            board.setx(50)
        else:
            board.setx(0)


    time.sleep(10000)



def main():
    turtle_triangle()


if __name__ == '__main__':
    main()