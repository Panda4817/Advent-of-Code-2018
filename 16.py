class Register():
    def __init__(self, register) -> None:
        self.registers = []
        self.update_registers(register)
        self.functions = [
            self.addi,
            self.addr,
            self.muli,
            self.mulr,
            self.banr,
            self.bani,
            self.borr,
            self.bori,
            self.setr,
            self.seti,
            self.gtir,
            self.gtri,
            self.gtrr,
            self.eqir,
            self.eqri,
            self.eqrr,
        ]
        self.opcodes = {i: set() for i in range(16)}

    def __str__(self) -> str:
        return f"{self.registers}"

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

    def check_same_register(self, after):
        n = 0
        if self.registers == after:
            n = 1
        return n

    def update_registers(self, before):
        self.registers.clear()
        for r in before:
            self.registers.append(r)

    def check_sample_three_or_more_opcodes(self, a, b, c, before, after):
        opcodes = 0
        for func in self.functions:
            func(a, b, c)
            opcodes += self.check_same_register(after)
            self.update_registers(before)

        if opcodes >= 3:
            return True

        return False

    def check_sample_and_update_opcodes(self, opcode, a, b, c, before, after):
        # If opcode already assigned a function, return
        if len(self.opcodes[opcode]) == 1:
            return

        # Go through each function, if opcode could be that function, add to list and keep count
        self.update_registers(before)
        to_add = []
        func_count = 0
        for func in self.functions:
            func(a, b, c)
            n = self.check_same_register(after)
            if n == 1:
                to_add.append(func)
                func_count += 1
            self.update_registers(before)

        # If count is 1 then that opcode can only be that function
        if func_count == 1:
            self.opcodes[opcode].clear()
            self.opcodes[opcode].add(to_add[0])

        # Else add each func to the opcode
        else:
            for func in to_add:
                self.opcodes[opcode].add(func)

    def refine_opcodes(self):
        done = set()
        while len(done) < 16:
            for k, v in self.opcodes.items():
                if isinstance(v, set):
                    l = list(v)
                    if len(v) == 1 and l[0] not in done:
                        func = l[0]
                        opcode = k
                        self.opcodes[k] = l[0]
                        break
                else:
                    if v not in done:
                        func = v
                        opcode = k
                        break

            for k, v in self.opcodes.items():
                if k == opcode:
                    continue

                if isinstance(v, set) and func in v:
                    self.opcodes[k].remove(func)

            done.add(func)

    def print_opcodes(self):
        try:
            for k, v in self.opcodes.items():
                print(k, [i.__name__ for i in v])
        except:
            for k, v in self.opcodes.items():
                print(k, v.__name__)

    def update_register_with_func(self, opcode, a, b, c):
        self.opcodes[opcode](a, b, c)


def process_data(data):
    parts = data.split("\n\n\n\n")
    samples = parts[0].split("\n\n")
    part1 = {}
    id = 0
    for sample in samples:
        lines = sample.split("\n")
        before = [int(i) for i in lines[0][9:19].split(", ")]
        options = [int(i) for i in lines[1].split()]
        opcode = options[0]
        a = options[1]
        b = options[2]
        c = options[3]
        after = [int(i) for i in lines[2][9:19].split(", ")]
        part1[id] = {
            "before": before,
            "opcode": opcode,
            "a": a,
            "b": b,
            "c": c,
            "after": after
        }
        id += 1

    test_program = [[int(j) for j in i.split()] for i in parts[1].split("\n")]

    return part1, test_program


def part1(data):
    samples, test_program = process_data(data)
    num_of_samples = 0
    for k, v in samples.items():
        register = Register(v["before"])
        if register.check_sample_three_or_more_opcodes(v["a"], v["b"], v["c"], v["before"], v["after"]):
            num_of_samples += 1

    return num_of_samples


def part2(data):
    samples, test_program = process_data(data)
    register = Register([0, 0, 0, 0])

    for k, v in samples.items():
        register.check_sample_and_update_opcodes(
            v["opcode"], v["a"], v["b"], v["c"], v["before"], v["after"])

    register.update_registers([0, 0, 0, 0])
    register.refine_opcodes()

    for command in test_program:
        register.update_register_with_func(
            command[0], command[1], command[2], command[3])

    return register.registers[0]
