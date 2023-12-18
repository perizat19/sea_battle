from random import randint, choice
from time import sleep


class BoardException(Exception):
    pass


class BoardWrongShipException(BoardException):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 


class BoardUsedException(BoardException):
    def __str__(self):
        return 


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    def __init__(self, bow: Dot, length: int, vertical: bool):
        self.bow = bow
        self.length = length
        self.vertical = vertical
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            curr_x = self.bow.x
            curr_y = self.bow.y
            if self.vertical:
                curr_y += i
            else:
                curr_x += i
            ship_dots.append(Dot(curr_x, curr_y))
        return ship_dots

    def is_hit(self, dot) -> bool:
        return dot in self.dots
