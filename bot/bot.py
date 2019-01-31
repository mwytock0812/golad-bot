import random

from field.point import Point
from move.move import Move
from move.move_type import MoveType


class Bot:

    def __init__(self):
        random.seed()  # set seed here if needed

    def make_move(self, game):
        """
        Performs a Birth or a Kill move, currently returns a random move.
        Implement this method to make the bot smarter.
        """
        cell_map = game.field.get_cell_mapping()

        if random.random() < 0.5:
            return self.make_random_birth_move(game, cell_map)
        else:
            return self.make_random_kill_move(game, cell_map)

    def make_random_birth_move(self, game, cell_map):
        dead_cells = cell_map.get('.', [])
        my_cells = cell_map.get(game.me.id, [])

        if len(dead_cells) <= 0 or len(my_cells) < 2:
            return self.make_random_kill_move(game, cell_map)

        random_birth = dead_cells[random.randrange(len(dead_cells))]

        sacrifices = self.my_dying_cells(game, cell_map)
        while len(sacrifices) < 2:
            sacrifices.append(my_cells.pop(random.randrange(len(my_cells))))

        return Move(MoveType.BIRTH, random_birth, sacrifices)

    def make_random_kill_move(self, game, cell_map):
        my_cells = cell_map.get(game.me.id, [])
        opponent_cells = cell_map.get(game.opponent.id, [])
        living_cells = my_cells + opponent_cells
        stable_cells = self.opponent_stable_cells(game, cell_map)

        if len(living_cells) <= 0 or len(stable_cells) <= 0:
            return Move(MoveType.PASS)
        stable_kill = stable_cells[random.randrange(len(stable_cells))]

        return Move(MoveType.KILL, stable_kill)

    def opponent_stable_cells(self, game, cell_map):
        stable = []
        opponent_cells = cell_map.get(game.opponent.id, [])
        for cell in opponent_cells:
            if self.living_neighbors(cell, game) in [2, 3]:
                stable.append(cell)
        return stable

    def my_dying_cells(self, game, cell_map):
        dying = []
        my_cells = cell_map.get(game.me.id, [])
        for cell in my_cells:
            if self.living_neighbors(cell, game) < 2:
                dying.append(cell)
        return dying

    def get_neighbors(self, cell, field):
        rows = [x for x in range(cell.x-1, cell.x+1)
                if x >= 0 and x < field.width]
        cols = [y for y in range(cell.y-1, cell.y+1)
                if y >= 0 and y < field.height]
        return [Point(x, y) for x in rows for y in cols]

    def living_neighbors(self, cell, game):
        count = 0
        neighbors = self.get_neighbors(cell, game.field)
        for n in neighbors:
            if n not in game.field.get_cell_mapping()['.']:
                count += 1
        return count
