import copy
import sys


class Register():
    def __init__(self, data, registers) -> None:
        self.registers = registers
        self.functions = {
            "addi": self.addi,
            "addr": self.addr,
            "muli": self.muli,
            "mulr": self.mulr,
            "banr": self.banr,
            "bani": self.bani,
            "borr": self.borr,
            "bori": self.bori,
            "setr": self.setr,
            "seti": self.seti,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr,
        }
        self.pointer = 0
        self.program, self.bound_to = self.process_data(data)

    def __str__(self) -> str:
        return f"{self.registers}{self.pointer}"

    def process_data(self, data):
        lines = data.split("\n")
        bound_to = int((lines[0].split())[1])
        program = {}
        n = 0
        for line in lines[1:]:
            parts = line.split()
            program[n] = {
                "name": parts[0],
                "a": int(parts[1]),
                "b": int(parts[2]),
                "c": int(parts[3])
            }
            n += 1

        return program, bound_to

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        if a > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtri(self, a, b, c):
        if self.registers[a] > b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtrr(self, a, b, c):
        if self.registers[a] > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqir(self, a, b, c):
        if a == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqri(self, a, b, c):
        if self.registers[a] == b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqrr(self, a, b, c):
        if self.registers[a] == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def update_register_with_func(self, name, a, b, c):
        self.functions[name](a, b, c)

    def run_program(self, max_times=None, until=False, p=False):
        # print(self)
        r = 0
        while self.pointer in self.program:

            # To run it a certain number of times
            if max_times and r == max_times:
                break

            # Main logic for the program
            self.registers[self.bound_to] = self.pointer
            v = self.program[self.pointer]
            self.update_register_with_func(v["name"], v["a"], v["b"], v["c"])
            self.pointer = self.registers[self.bound_to] + 1

            # Debugging and testing, to stop it running forever
            if until and self.registers[5] >= self.registers[2] and self.registers[2] != 0:
                break

            # To print
            if p:
                print(v, self)
                print()

            r += 1


def part1(data):
    registers = Register(data, [0, 0, 0, 0, 0, 0])
    registers.run_program(max_times=20)
    reg = registers.registers[2]
    slot_0 = 0
    divider = 1
    while True:
        if reg % divider == 0:
            slot_0 += divider
            if reg / divider == 1.0:
                break
        divider += 1
    return slot_0


def part2(data):
    registers = Register(data, [1, 0, 0, 0, 0, 0])
    registers.run_program(max_times=20)
    reg = registers.registers[2]
    slot_0 = 0
    divider = 1
    while True:
        if reg % divider == 0:
            slot_0 += divider
            if reg / divider == 1.0:
                break
        divider += 1
    return slot_0
