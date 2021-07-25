import z3

# I tried other packages to help with part 2
import numpy as np
from queue import PriorityQueue
from sys import maxsize
from scipy import spatial
from copy import deepcopy
from itertools import combinations


class Object():
    def __init__(self, x, y, z, r) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __str__(self) -> str:
        return f"pos=<{self.x},{self.y},{self.z}>, r={self.r}"

    def __eq__(self, o: object) -> bool:
        return o.x == self.x and o.y == self.y and o.z == self.z and o.r == self.r

    def update_pos(self, x, y, z, r=None):
        self.x = x
        self.y = y
        self.z = z
        if r:
            self.r = r

    def return_tuple(self):
        return (self.x, self.y, self.z)

    def mh(self, other):
        return abs(self.x-other.x) + abs(self.y - other.y) + abs(self.z-other.z)

    def total_in_range_with_self(self, others):
        in_range_count = 0
        for other in others:
            mh = self.mh(other)
            if mh <= self.r:
                in_range_count += 1
        return in_range_count


def process_data(data):
    lines = data.split("\n")
    nanobots = []
    strongest: Object = None
    for line in lines:
        pos, r = line.split(", ")
        x, y, z = [int(i) for i in pos[5:-1].split(",")]
        radius = int(r[2:])
        nanobot = Object(x, y, z, radius)
        nanobots.append(nanobot)
        if strongest and nanobot.r > strongest.r:
            strongest = nanobot
        elif not strongest:
            strongest = nanobot

    return nanobots, strongest


def part1(data):
    nanobots, strongest = process_data(data)
    return strongest.total_in_range_with_self(nanobots)


def part2(data):
    nanobots, strongest = process_data(data)
    # For part 2 I tried a priority queue and various packages to find nearest bots for a specific coordinate
    # Best result with z3 solver (hint from reddit)
    x = z3.Int('x')
    y = z3.Int('y')
    z = z3.Int('z')

    def abs(x):
        return z3.If(x >= 0, x, -x)

    s = z3.Optimize()
    for n in nanobots:
        s.add_soft(abs(x-n.x) + abs(y-n.y) + abs(z-n.z) <= n.r)

    if str(s.check()) == "sat":
        m = s.model()
        return m.evaluate(abs(x) + abs(y) + abs(z))
