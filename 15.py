from collections import deque
from copy import deepcopy
import sys
from typing import List


class Unit():
    def __init__(self, x, y, attack_power) -> None:
        self.current_x = x
        self.current_y = y
        self.hit_points = 200
        self.attack_power = attack_power


class Elf(Unit):
    def __init__(self, x, y, attack_power) -> None:
        super().__init__(x, y, attack_power)
        self.target = Goblin

    def __str__(self) -> str:
        return "E"

    def print_info(self):
        return f"E{self.current_x, self.current_y}{self.hit_points, self.attack_power}"


class Goblin(Unit):
    def __init__(self, x, y, attack_power) -> None:
        super().__init__(x, y, attack_power)
        self.target = Elf

    def __str__(self) -> str:
        return "G"

    def print_info(self):
        return f"G{self.current_x, self.current_y}{self.hit_points, self.attack_power}"


class GameBoard():
    def __init__(self) -> None:
        self.board = []
        self.elves = 0
        self.goblins = 0
        self.rounds = 0

    def __str__(self) -> str:
        string = ""
        for line in self.board:
            string += "".join([i.__str__() if isinstance(i,
                              Unit) else i for i in line])
            for l in line:
                if isinstance(l, Unit):
                    string += " " + l.print_info()
            string += "\n"
        return string

    def get_adjacent_cells(self, cell_x, cell_y):
        x = [0, -1, 1, 0]
        y = [-1, 0, 0, 1]
        cells = []
        for i, j in zip(x, y):
            cells.append((cell_x + i, cell_y + j))
        return cells

    def process_data(self, data, elf_attack_power, goblin_attack_power):
        lines = data.split("\n")
        y = 0
        for line in lines:
            row = []
            x = 0
            for part in line:
                if part == "#" or part == ".":
                    row.append(part)
                elif part == "E":
                    elf = Elf(x, y, elf_attack_power)
                    row.append(elf)
                    self.elves += 1
                else:
                    goblin = Goblin(x, y, goblin_attack_power)
                    row.append(goblin)
                    self.goblins += 1
                x += 1
            self.board.append(row)
            y += 1

    def get_path(self, dest, path_dict):
        final_path = []
        length = 0
        current = dest
        while current != None:
            final_path.append(current)
            length += 1
            current = path_dict[current]
        return final_path, length

    def get_shortest_path(self, unit, destinations: List):
        q = deque()

        q.append((unit.current_x, unit.current_y))
        explored = [(unit.current_x, unit.current_y)]
        path = {(unit.current_x, unit.current_y): None}
        dest = None
        current_path_length = sys.maxsize
        current_final_path = None

        while q:

            x, y = q.popleft()

            if (x, y) in destinations:
                final_path, length = self.get_path((x, y), path)
                if length < current_path_length or dest == None or (destinations.index((x, y)) < destinations.index(dest) and length <= current_path_length):
                    current_path_length = length
                    current_final_path = final_path
                    dest = (x, y)

            cells = self.get_adjacent_cells(x, y)

            for (i, j) in cells:
                if (i, j) not in explored and self.board[j][i] == ".":
                    path[(i, j)] = (x, y)
                    q.append((i, j))
                    explored.append((i, j))

        return current_final_path

    def choose_square(self, unit):
        destinations = []
        board = deepcopy(self.board)
        # go through the board:
        for row in self.board:
            for col in row:
                # if target, add adjacent cells to list
                if isinstance(col, unit.target):
                    cells = self.get_adjacent_cells(
                        col.current_x, col.current_y)

                    # for each adjacent cell
                    # is it viable, yes- add to copied board
                    for (x, y) in cells:
                        if self.board[y][x] == ".":
                            board[y][x] = "D"

        # Insert the viable cells to list in reading order
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == "D":
                    destinations.append((x, y))

        final_path = self.get_shortest_path(unit, destinations)

        return final_path

    def move(self, unit):
        # choose_square
        chosen = self.choose_square(unit)
        if not chosen:
            return unit
        x, y = chosen[-2]

        # remove unit from square and update board
        self.board[unit.current_y][unit.current_x] = "."
        unit.current_x = x
        unit.current_y = y
        self.board[unit.current_y][unit.current_x] = unit
        return unit

    def attack(self, unit, target):
        # print(unit.print_info(), "attacking", target.print_info())
        target.hit_points -= unit.attack_power
        if target.hit_points <= 0:
            self.board[target.current_y][target.current_x] = "."
            if unit.target == Goblin:
                self.goblins -= 1
            elif unit.target == Elf:
                self.elves -= 1
        else:
            self.board[target.current_y][target.current_x].hit_points = target.hit_points

    def check_within_range(self, unit):
        cells = self.get_adjacent_cells(unit.current_x, unit.current_y)
        fewest_hp = 200
        selected = None
        for (x, y) in cells:
            if isinstance(self.board[y][x], unit.target):
                if self.board[y][x].hit_points < fewest_hp:
                    selected = self.board[y][x]
                    fewest_hp = selected.hit_points
                elif self.board[y][x].hit_points == fewest_hp and selected == None:
                    selected = self.board[y][x]
        return selected

    def turn(self, unit):
        # check unit still alive, if not end turn
        for row in self.board:
            if unit in row:
                break
        else:
            return True

        # check if target in range, if so go to attack, else go to move, then attack
        selected = self.check_within_range(unit)

        if not selected:

            unit = self.move(unit)

            selected = self.check_within_range(unit)

            if not selected:
                return True

        self.attack(unit, selected)
        return True

    def get_total_hit_points(self):
        total = 0
        for row in self.board:
            for col in row:
                if isinstance(col, Unit):
                    total += col.hit_points
        return total

    def play_part1(self):
        # while board has elves and goblins (if one team remain then break out of while)
        while self.goblins > 0 and self.elves > 0:
            # print("Start of ", self.rounds + 1)
            # go through and identify which units are alive
            alive = []
            for row in self.board:
                for col in row:
                    if isinstance(col, Unit) and col.hit_points > 0:
                        alive.append(col)

            # Each of those units have their turn
            turns_completed = 0
            length = len(alive)
            for unit, i in zip(alive, range(length)):
                # check the board for targets, if none, end game
                if unit.target == Goblin and self.goblins == 0:
                    break
                elif unit.target == Elf and self.elves == 0:
                    break

                self.turn(unit)
                turns_completed += 1

            # increase round number if all units had turn
            # if turns_completed == len(alive):
            if turns_completed == length:
                self.rounds += 1
            # print(self)

        # return outcome rounds multiplied by total hit_points
        print(self.rounds)
        total_hits = self.get_total_hit_points()
        print(total_hits)
        return self.rounds * total_hits

    def play_part2(self):
        # Establish total_elves
        total_elves = self.elves

        # while board has elves and goblins (if one team remain then break out of while)
        while self.goblins > 0 and self.elves == total_elves:
            # print("Start of ", self.rounds + 1)
            # go through and identify which units are alive
            alive = []
            for row in self.board:
                for col in row:
                    if isinstance(col, Unit) and col.hit_points > 0:
                        alive.append(col)

            # Each of those units have their turn
            turns_completed = 0
            length = len(alive)
            for unit, i in zip(alive, range(length)):
                # check the board for targets, if none, end game
                if unit.target == Goblin and self.goblins == 0:
                    break
                elif unit.target == Elf and self.elves == 0:
                    break
                self.turn(unit)
                turns_completed += 1

            # increase round number if all units had turn
            # if turns_completed == len(alive):
            if turns_completed == length:
                self.rounds += 1
            # print(self)

        # return outcome rounds multiplied by total hit_points
        # If an elf died, return 0
        if self.elves < total_elves:
            return 0
        print(self.rounds)
        total_hits = self.get_total_hit_points()
        print(total_hits)
        return self.rounds * total_hits


def part1(data):
    game = GameBoard()
    game.process_data(data, 3, 3)
    # print(game)
    outcome = game.play_part1()
    return outcome


def part2(data):
    # ap is attack power of elves
    ap = 4
    while True:
        game = GameBoard()
        game.process_data(data, ap, 3)
        outcome = game.play_part2()
        if outcome > 0:
            break
        ap += 1

    return outcome
