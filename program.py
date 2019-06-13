# a program to divide the board of Kolonisten of Catan semi-evenly
# this means that every spot has about the same weight and chance of getting a good spot

import turtle
import time
from pprint import pprint

import board_calculator

polygon_angle = 120

polygon_base = 100


def draw_board(turtle_board, calced_board):
    for x, x_list in enumerate(calced_board):  # loop depth of board for drawing
        for y, val in enumerate(x_list):  # loop length of board for drawing
            draw_hexagon(val, turtle_board)
        turtle_board.penup()
        turtle_board.sety(-((x + 1) * 86.60))  # prep y-axis for next triangle
        if x % 2 == 0:  # prep x-axis for next triangle
            turtle_board.setx(-50)
        else:
            turtle_board.setx(0)


def draw_hexagon(val, turtle_board: turtle.Turtle) -> None:
    hexagon_side = 57.735
    if val is None:
        turtle_board.write('')
    else:
        valstr = f'{val[0]}, {val[2]}'
        turtle_board.write(valstr)
    turtle_board.penup()

    turtle_board.forward(50)
    turtle_board.pendown()
    turtle_board.left(90)
    turtle_board.forward(hexagon_side / 2)
    for i in range(0, 5):
        turtle_board.left(60)
        turtle_board.forward(hexagon_side)
    turtle_board.left(60)
    turtle_board.forward(hexagon_side / 2)
    turtle_board.penup()
    turtle_board.left(270)
    turtle_board.forward(50)
    turtle_board.pendown()


def main():
    calced_board = board_calculator.calculate_weights()
    pprint(calced_board)
    turtle_board = turtle.Turtle()
    draw_board(turtle_board, calced_board)
    time.sleep(4000)


if __name__ == '__main__':
    main()
