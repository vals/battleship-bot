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
    and methods to perform moves.
    """
    def __init__(self, size=10, sizes=[5, 4, 3, 3, 2]):
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

    def play(self, coord):
        """Play a move in the game with the coordinate as a tuple of integers.
        Returns True if a ship is hit, False otherwise.
        """
        for ship in self.ships:
            if coord in ship.hull:
                return True

        return False


class Strategy(object):
    """Represents a strategy used by a battleship bot to win the game by
    finding all the ships.
    """
    def __init__(self, total=17):
        self.hits = []
        self.misses = []
        self.total = total


class RandomStrategy(Strategy):
    """A silly strategy where moves are picked completely at random"""
    def __init__(self, game, total=17):
        super(RandomStrategy, self).__init__(total)
        self.game = game

    def run(self):
        all_coords = []
        for i in range(10):
            for j in range(10):
                all_coords.append((i, j))

        while len(self.hits) < self.total:
            coord = random.choice(all_coords)
            all_coords.remove(coord)

            if self.game.play(coord):
                self.hits.append(coord)
            else:
                self.misses.append(coord)

        return len(self.hits) + len(self.misses)


class RandomGuidedStrategy(Strategy):
    """Looks at neighbours of randomly found hits"""
    def __init__(self, game, total=17):
        super(RandomGuidedStrategy, self).__init__(total)
        self.game = game

    def run(self):
        all_coords = []
        for i in range(10):
            for j in range(10):
                all_coords.append((i, j))

        while len(self.hits) < self.total:
            coord = random.choice(all_coords)
            all_coords.remove(coord)

            if self.game.play(coord):
                self.hits.append(coord)
                n_hits = 1
                while coord[0] < 9:
                    coord = (coord[0] + 1, coord[1])
                    if coord not in all_coords:
                        break
                    if not self.game.play(coord):
                        self.misses.append(coord)
                        all_coords.remove(coord)
                        break
                    else:
                        self.hits.append(coord)
                        all_coords.remove(coord)
                        n_hits += 1

                if n_hits > 1:
                    continue

                while coord[1] < 9:
                    coord = (coord[0], coord[1] + 1)
                    if coord not in all_coords:
                        break
                    if not self.game.play(coord):
                        self.misses.append(coord)
                        all_coords.remove(coord)
                        break
                    else:
                        self.hits.append(coord)
                        all_coords.remove(coord)
                        n_hits += 1

                if n_hits > 1:
                    continue

                while coord[0] > 0:
                    coord = (coord[0] + 1, coord[1])
                    if coord not in all_coords:
                        break
                    if not self.game.play(coord):
                        self.misses.append(coord)
                        all_coords.remove(coord)
                        break
                    else:
                        self.hits.append(coord)
                        all_coords.remove(coord)
                        n_hits += 1

                if n_hits > 1:
                    continue

                while coord[1] > 0:
                    coord = (coord[0], coord[1] + 1)
                    if coord not in all_coords:
                        break
                    if not self.game.play(coord):
                        self.misses.append(coord)
                        all_coords.remove(coord)
                        break
                    else:
                        self.hits.append(coord)
                        all_coords.remove(coord)
                        n_hits += 1
            else:
                self.misses.append(coord)

        return len(self.hits) + len(self.misses)

## RUNNING ##
s = 0
for i in range(1000):
    game = Game()
    strategy = RandomGuidedStrategy(game)
    s += strategy.run()

print(s / 1000)
game.print_ships()
