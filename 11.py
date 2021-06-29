def get_serial(data):
    return int(data)


def get_all_power_levels(serial, cells):
    grid = []
    highest = 0
    highest_x = 0
    highest_y = 0
    total = 0
    for y in range(1, cells + 1):
        row = []
        for x in range(1, cells + 1):
            rack_id = x + 10
            power = rack_id * y
            power += serial
            power *= rack_id
            n = list(str(power))
            n.reverse()
            if len(n) < 3:
                p = 0 - 5
            else:
                p = int(n[2]) - 5

            if p > highest:
                highest = p
                highest_x = x
                highest_y = y
            total += p
            row.append(p)
        grid.append(row)
    return grid, highest, highest_x, highest_y, total


def part1(data):
    serial = get_serial(data)
    cells = 300
    grid, highest_power, X, Y, total_of_all_cells = get_all_power_levels(
        serial, cells)

    for r in range(0, cells):
        if r > cells - 4:
            break
        for c in range(0, cells):
            if c > cells - 4:
                break

            total = 0
            for y in range(r, r+3):
                for x in range(c, c+3):
                    total += grid[y][x]
            if total > highest_power:
                highest_power = total
                X = c + 1
                Y = r + 1
    return X, Y, highest_power


def part2(data):
    serial = get_serial(data)
    cells = 300
    grid, highest_power, X, Y, all_cells_total = get_all_power_levels(
        serial, cells)
    size = 1

    for r in range(0, cells):
        for c in range(0, cells):
            lower = 0  # a number to limit the range of square sizes to try
            for s in range(2, cells):
                if r > cells - s or c > cells - s:
                    break
                total = 0
                for y in range(r, r+s):
                    for x in range(c, c+s):
                        total += grid[y][x]
                if total > highest_power:
                    highest_power = total
                    X = c + 1
                    Y = r + 1
                    size = s
                else:
                    lower += 1
                    if lower > 15:
                        break

    if all_cells_total > highest_power:
        highest_power = all_cells_total
        X = 1
        Y = 1
        size = 300

    return X, Y, size, highest_power
