from tabulate import tabulate


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
        return f"{self.registers}"

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

        # to_print = [
        #     ["method", "r/i", "r/i", "=>reg", "reg0", "reg1",
        #         "reg2", "reg3", "reg4", "reg5", "ip", "total"],
        # ]

        while self.pointer in self.program:

            # This will tell you what slot_0 needs to be to halt program
            if self.pointer == 28:
                print(self, r)

            # To run it a certain number of times
            # if max_times and r == max_times:
            #     break

            # Main logic for the program
            self.registers[self.bound_to] = self.pointer
            v = self.program[self.pointer]
            self.update_register_with_func(v["name"], v["a"], v["b"], v["c"])
            self.pointer = self.registers[self.bound_to] + 1

            # Debugging and testing, to stop it running forever
            # if until and self.registers[5] >= self.registers[2] and self.registers[2] != 0:
            #     break

            # To print
            # if p:
            #     to_print.append([
            #         v["name"],
            #         v["a"],
            #         v["b"],
            #         v["c"],
            #         self.registers[0],
            #         self.registers[1],
            #         self.registers[2],
            #         self.registers[3],
            #         self.registers[4],
            #         self.registers[5],
            #         self.pointer,
            #         r
            #     ])

            r += 1

        # if p:
        #     print(tabulate(to_print, headers="firstrow", tablefmt="github"))
        return r


def part1(data):
    # Part 1 7224964, Part 2 13813247
    # slot_0 = 13813247
    # register = Register(data, [slot_0, 0, 0, 0, 0, 0])
    # rounds = register.run_program(p=True)
    # print(rounds)

    b = 0
    a = 0
    a = b | 65536
    b = 13284195
    b += a & 255
    b = b & 16777215
    b = b * 65899
    b = b & 16777215
    possible_slot0 = []
    while True:
        a = a // 256
        b += a & 255
        b = b & 16777215
        b = b * 65899
        b = b & 16777215
        if 256 > a:
            # Break for part 1 and return b
            if b not in possible_slot0:
                possible_slot0.append(b)
            else:
                # Break for part 2 and return last value in list
                break
            a = b | 65536
            b = 13284195
            b += a & 255
            b = b & 16777215
            b = b * 65899
            b = b & 16777215

    return possible_slot0[0], possible_slot0[-1]
