class Ground():
    def __init__(self, data) -> None:
        self.spring = (500, 0)
        self.map, self.min_x, self.max_x, self.max_y, self.min_y = self.process_data(
            data)

    def __str__(self) -> str:
        ansi_grey = "\033[30m\033[40m"
        ansi_yellow = "\033[33m\033[43m"
        ansi_blue = "\033[34m\033[44m"
        ansi_cyan = "\033[36m\033[46m"
        ansi_clear = "\033[0m"
        string = ""
        for r in range(0, self.max_y+1):
            for c in range(self.min_x-1, self.max_x+1):
                if self.map[r][c] == '.':
                    string += ansi_yellow
                elif self.map[r][c] == '#':
                    string += ansi_grey
                elif self.map[r][c] == '~':
                    string += ansi_blue
                elif self.map[r][c] in ('|', '+'):
                    string += ansi_cyan
                string += self.map[r][c] + ansi_clear
            string += "\n"
        return string

    def process_data(self, data):
        map = []
        lines = [line.split(", ") for line in data.split("\n")]
        x_numbers = set()
        y_numbers = set()
        clay = []

        for line in lines:
            for val in line:
                parts = val.split("=")
                numbers = [int(i) for i in parts[1].split("..")]
                if parts[0] == "x":
                    x = numbers
                    x_numbers.update(set(numbers))
                else:
                    y = numbers
                    y_numbers.update(set(numbers))

            if len(x) == 1:
                for i in range(y[0], y[1]+1):
                    clay.append((x[0], i))
            else:
                for i in range(x[0], x[1]+1):
                    clay.append((i, y[0]))

        max_x = max(x_numbers)
        max_y = max(y_numbers)

        for r in range(0, max_y + 1):
            row = ["." for c in range(0, max_x + 2)]
            map.append(row)

        map[self.spring[1]][self.spring[0]] = "+"
        for coord in clay:
            map[coord[1]][coord[0]] = "#"

        return map, min(x_numbers), max_x, max_y, min(y_numbers)

    def bucket_or_overspill(self, x, y):
        result = []
        down_reached_left = None
        down_reached_right = None
        left_x = x

        while self.map[y][left_x] != "#" and down_reached_left == None:
            left_x -= 1

            if self.map[y+1][left_x] == "." or self.map[y+1][left_x] == "|":
                down_reached_left = left_x

        if down_reached_left == None:
            result.append(False)
            result.append(left_x+1)
        else:
            result.append(True)
            result.append(left_x)

        right_x = x

        while self.map[y][right_x] != "#" and down_reached_right == None:
            right_x += 1

            if self.map[y+1][right_x] == "." or self.map[y+1][right_x] == "|":
                down_reached_right = right_x

        if down_reached_right == None:
            result.append(right_x)
            result.append(False)
        else:
            result.append(right_x+1)
            result.append(True)

        if result[0] == False and result[3] == False:
            result.append(True)
        else:
            result.append(False)

        return result

    def reached_end(self, water_pos):
        for (x, y) in water_pos:
            if y >= self.max_y:
                return True

        return False

    def count_water_squares(self):
        counter_part1 = 0
        counter_part2 = 0
        for y in range(self.min_y, self.max_y+1):
            for c in range(self.min_x - 1, self.max_x + 1):
                if self.map[y][c] == "|" or self.map[y][c] == "~":
                    counter_part1 += 1

                if self.map[y][c] == "~":
                    counter_part2 += 1
        return counter_part1, counter_part2

    def start_spring(self):
        water_pos = set([self.spring])
        while self.reached_end(water_pos) == False:
            update = []
            for (x, y) in water_pos:
                if self.map[y+1][x] == ".":
                    update.append([(x, y), (x, y+1)])
                    self.map[y+1][x] = "|"
                elif self.map[y+1][x] == "#" or self.map[y+1][x] == "~":
                    result = self.bucket_or_overspill(x, y)
                    if result[4] == True:
                        for i in range(result[1], result[2]):
                            self.map[y][i] = "~"

                        update.append([(x, y), (x, y-1)])
                    else:
                        if result[0] == True:
                            update.append([(x, y), (result[1], y+1)])
                            self.map[y+1][result[1]] = "|"

                        if result[3] == True:
                            update.append([(x, y), (result[2]-1, y+1)])
                            self.map[y+1][result[2]-1] = "|"

                        for i in range(result[1], result[2]):
                            self.map[y][i] = "|"

            for pos in update:
                if pos[0] in water_pos:
                    water_pos.remove(pos[0])

                water_pos.add(pos[1])
            # print(self)

        water_count_part1, water_count_part2 = self.count_water_squares()
        return water_count_part1, water_count_part2


# part 1 and 2 in same function
def part1(data):
    ground = Ground(data)
    # print(ground)
    part1, part2 = ground.start_spring()
    # print(ground)
    return part1, part2
