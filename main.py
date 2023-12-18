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

class Board:
    def __init__(self, size: int, hid=False):
        self.size = size
        self.hid = hid
        self.field = [['O'] * size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.last_hit = []      
        self.count_destr_ships = 0      

    def __str__(self):
        res = '  | ' + ' | '.join(map(str, range(1, self.size + 1))) + ' |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' |'
        if self.hid:
            res = res.replace('■', 'O')
        return res

    def out(self, d: Dot) -> bool:
        return not (0 <= d.x < self.size and 0 <= d.y < self.size)

    def contour(self, ship, visible=False):
        around = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        for dot in ship.dots:
            for dx, dy in around:
                curr_dot = Dot(dot.x + dx, dot.y + dy)
                if not self.out(curr_dot) and curr_dot not in self.busy:
                    if visible:      
                        self.field[curr_dot.x][curr_dot.y] = '.'
                    self.busy.append(curr_dot)

    def add_ship(self, ship):
        for d in ship.dots:
            if d in self.busy or self.out(d):
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d: Dot) -> bool:    
        if d in self.busy:
            raise BoardUsedException()
        if self.out(d):
            raise BoardOutException()
        self.busy.append(d)

        for ship in self.ships:
            if ship.is_hit(d):
                self.field[d.x][d.y] = 'X'
                print('Hitted!')
                ship.lives -= 1
                if ship.lives == 0:
                    self.count_destr_ships += 1
                    self.contour(ship, visible=True)
                    print('Sunk!')
                    self.last_hit = []
                    return False
                else:
                    print('Hitted!')
                    self.last_hit.append(d)
                    return True

        self.field[d.x][d.y] = '.'
        print('Miss!')
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count_destr_ships == len(self.ships)

class Player:
    def __init__(self, board: Board, enemy: Board):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self) -> bool:   
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                sleep(1)
                return repeat
            except BoardException as excep:
                print(excep)

class AI(Player):
    def ask(self) -> Dot:
        last = self.enemy.last_hit
        while True:
            if last:    
                if len(last) == 1:
                    near = ((0, 1), (0, -1), (1, 0), (-1, 0))
                else:
                    if last[0].x == last[-1].x:
                        near = ((0, 1), (0, -1))
                    else:
                        near = ((1, 0), (-1, 0))
                dx, dy = choice(near)
                d = choice((Dot(last[-1].x + dx, last[-1].y + dy), Dot(last[0].x + dx, last[0].y + dy)))
            else:
                d = Dot(randint(0, 5), randint(0, 5))
            if d not in self.enemy.busy and not self.enemy.out(d):
                break
        sleep(0.1 * randint(15, 50))   
        print(f"Computer's step: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self) -> Dot:
        while True:
            coords = input('Enter shoot coordinates:\t').split()
            if len(coords) != 2:
                print('Enter 2 coordinates')
                continue
            x, y = coords
            if not all((x.isdigit(), y.isdigit())):
                print('Coordinates must be numbes')
                continue
            return Dot(int(x) - 1, int(y) - 1)