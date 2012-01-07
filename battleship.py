"""Investigating the efficiency of simply battleship strategies.
"""
import random
import numpy as np


class Ship():
    """Class representing a ship.
    """
    def __init__(self, size):
        self.size = size
        self.hull = set([])

    def place(self, illegal):
        """Randomly place the ship.
        The argument illiegal is a set of points in the grid where
        the ship is not allowed    to go.
        """
        placed = False
        while not placed:
            wake = set([])
            self.hull = set([])
            bow = np.array([np.random.randint(10), np.random.randint(10)])

            try:
                if tuple(bow) in illegal:
                    raise Exception("Ship cannot go there")

                axis = random.choice([np.array([1, 0]), np.array([0, 1])])
                # direction = random.choice([1,-1])
                direction = 1

                wake.add(tuple(bow + direction * (1 - axis)))
                wake.add(tuple(bow - direction * (1 - axis)))

                wake.add(tuple(bow - direction * axis + (1 - axis)))
                wake.add(tuple(bow - direction * axis))
                wake.add(tuple(bow - direction * axis - (1 - axis)))

                self.hull.add(tuple(bow))

                for part in range(1, self.size):
                    square = bow + part * direction * axis

                    if np.any(square > 9) or np.any(square <= 0) or \
                    tuple(square) in illegal:
                        raise Exception("Ship cannot go there")

                    wake.add(tuple(square + direction * (1 - axis)))
                    wake.add(tuple(square - direction * (1 - axis)))

                    self.hull.add(tuple(square))

                wake.add(tuple(square + direction * axis + (1 - axis)))
                wake.add(tuple(square + direction * axis))
                wake.add(tuple(square + direction * axis - (1 - axis)))

                placed = True

            except Exception:
                pass

        illegal = illegal.union(wake)
        illegal = illegal.union(self.hull)
        return illegal

    def __str__(self):
        """Display the ships hull on a grid represented by a
        numpy array.
        """
        board = np.ones((10, 10))
        for coord in self.hull:
            try:
                board[coord[0], coord[1]] = 0
            except IndexError:
                pass

        return str(board)


class Game(object):
    """Models a game of battleship, contains a board on which ships are placed,
    and methods to perform modes.
    """
    def __init__(self, size=10):
        sizes = [5, 4, 3, 3, 2]
        self.generate_ships(sizes)
        self.place_ships()

    def generate_ships(self, sizes):
        """Return a list of Ships.
        """
        self.ships = []
        for size in sizes:
            self.ships.append(Ship(size))

    def place_ships(self):
        """Place ship on the board.
        """
        illegal = set([])
        for ship in self.ships:
            illegal = ship.place(illegal)

    def print_ships(self):
        """Display an array representation of the ship placements.
        """
        board = np.ones((10, 10))
        for ship in self.ships:
            try:
                for coord in ship.hull:
                    try:
                        board[coord[0], coord[1]] = 0
                    except IndexError:
                        pass
            except AttributeError:
                pass

        print(board)


# class Strategy(object):
#     """Represents a strategy used by a battleship bot to win the game by
#     finding all the ships.
#     """
#     self.on_hit = lambda: None
#     self.on_miss = lambda: None
#     self.hits = []
#     self.misses = []

## RUNNING ##
game = Game()
game.print_ships()
