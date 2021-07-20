class Land():
    def __init__(self, data, rows, cols) -> None:
        self.map = [list(row) for row in data.split("\n")]
        self.rows = rows
        self.cols = cols
        self.trees = sum([row.count("|") for row in self.map])
        self.lumberyards = sum([row.count("#") for row in self.map])

    def __str__(self) -> str:
        string = ""
        for row in self.map:
            string += "".join(row) + "\n"
        return string

    def get_adjacent_acres(self, x, y):
        cells = []
        for j in range(-1, 2):
            r = y + j
            if r < 0 or r >= self.rows:
                continue
            for i in range(-1, 2):
                c = x + i
                if c < 0 or c >= self.cols:
                    continue

                if (c, r) == (x, y):
                    continue

                cells.append((c, r))
        return cells

    def is_tree(self, x, y):
        adjacent_cells = self.get_adjacent_acres(x, y)
        tree_count = 0
        for (i, j) in adjacent_cells:
            if self.map[j][i] == "|":
                tree_count += 1

        if tree_count >= 3:
            return True

        return False

    def is_lumberyard(self, x, y):
        adjacent_cells = self.get_adjacent_acres(x, y)
        lumberyard_count = 0
        for (i, j) in adjacent_cells:
            if self.map[j][i] == "#":
                lumberyard_count += 1

        if lumberyard_count >= 3:
            return True

        return False

    def is_open(self, x, y):
        adjacent_cells = self.get_adjacent_acres(x, y)
        lumberyard_count = 0
        tree_count = 0
        for (i, j) in adjacent_cells:
            if self.map[j][i] == "#":
                lumberyard_count += 1
            elif self.map[j][i] == "|":
                tree_count += 1

        if lumberyard_count >= 1 and tree_count >= 1:
            return False

        return True

    def change_landscape(self, minutes):
        for m in range(1, minutes+1):
            new_land = []
            for y in range(self.rows):
                row = []
                for x in range(self.cols):
                    if self.map[y][x] == "." and self.is_tree(x, y):
                        row.append("|")
                        self.trees += 1
                    elif self.map[y][x] == "|" and self.is_lumberyard(x, y):
                        row.append("#")
                        self.trees -= 1
                        self.lumberyards += 1
                    elif self.map[y][x] == "#" and self.is_open(x, y):
                        row.append(".")
                        self.lumberyards -= 1
                    else:
                        row.append(self.map[y][x])
                new_land.append(row)
            self.map = new_land
            # print(self, m, self.trees, self.lumberyards)


def part1(data):
    minutes = 10
    acres = 50
    land = Land(data, acres, acres)
    print(land)
    land.change_landscape(minutes)
    return land.trees * land.lumberyards


def part2(data):
    real_minutes = 1000000000
    resources = {}
    acres = 50
    land_test = Land(data, acres, acres)
    lowest_test_min = 100
    highest_test_min = 500  # Can change this to higher number to see the pattern
    land_test.change_landscape(lowest_test_min)
    resources[lowest_test_min] = (land_test.trees, land_test.lumberyards)
    pairs_of_same_resources = []
    m = lowest_test_min + 1
    while m != highest_test_min + 1:
        land_test.change_landscape(1)
        if (land_test.trees, land_test.lumberyards) in resources.values():
            m2 = m
            for k, v in resources.items():
                if v == (land_test.trees, land_test.lumberyards):
                    m1 = k
                    break
            pairs_of_same_resources.append((m1, m2))

        resources[m] = (land_test.trees, land_test.lumberyards)
        m += 1

    print(pairs_of_same_resources)

    # from the pairs_of_same_resources I can see a number pattern
    mins = real_minutes - 455
    loop_repeats_every = 28
    leftover = mins % loop_repeats_every
    final_mins = 455 + leftover
    print(mins, loop_repeats_every, leftover, final_mins)
    (trees, lumberyards) = resources[final_mins]
    return trees * lumberyards
