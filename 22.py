import tabulate
from queue import PriorityQueue


def geologic_index(x, y, target, erosion_map):
    # Calculate the geological index
    if (0, 0) == (x, y) or target == (x, y):
        return 0

    if y == 0:
        return x * 16807

    if x == 0:
        return y * 48271

    val1 = erosion_map[y][x-1]
    val2 = erosion_map[y-1][x]

    return val1 * val2


def erosion_level(geological_index, depth):
    # Calculate erosion level
    return (geological_index + depth) % 20183


def create_maps(max_x, max_y, depth, target):
    # Create 3 maps of the cave to calculate the risk level
    geologic_map = []
    erosion_map = []
    risk_map = []
    for i in range(max_y + 1):
        geo = []
        ero = []
        risk = []
        for j in range(max_x+1):
            geo.append(0)
            ero.append(0)
            risk.append(0)
        geologic_map.append(geo)
        erosion_map.append(ero)
        risk_map.append(risk)

    x = 0
    risk_total = 0

    while x < max_x:

        for y in range(0, max_y):
            g_index = geologic_index(x, y, target, erosion_map)
            erosion = erosion_level(g_index, depth)
            risk = erosion % 3

            geologic_map[y][x] = g_index
            erosion_map[y][x] = erosion
            risk_map[y][x] = risk

            # Part 1
            risk_total += risk

        x += 1

    return risk_total, risk_map


def part1(data):
    depth = 4080
    target = (14, 785)
    risk_total, risk_map = create_maps(target[0]+1, target[1]+1, depth, target)

    return risk_total


def in_bounds(x, y, x_depth, y_depth):
    # Check if adjacent cells are within the grid
    if x >= 0 and x < x_depth and y > 0 and y < y_depth:
        return True

    return False


def get_adjacent_cells(x, y, x_depth, y_depth):
    # Get adjacent cells in a grid
    cells = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]

    res = []
    for (i, j) in cells:
        if in_bounds(i, j, x_depth, y_depth):
            res.append((i, j))

    return res


def print_map(map, x, y, target, visited=None, equip=None, backtrack=True, path=False):
    # Print grid with visited cells and path
    # ansi_grey = "\033[30m\033[40m"
    # ansi_blue = "\033[34m\033[44m"
    # ansi_cyan = "\033[36m\033[46m"
    ansi_yellow = "\033[33m"
    ansi_clear = "\033[0m"
    ansi_red = "\033[91m"
    ansi_green = "\033[92m"
    draw = {
        0: ".",
        1: "=",
        2: "|"
    }
    # Add visited cells and path
    if visited and equip:
        l = set([k[0] for k in visited.keys()])
        max_y = max(l, key=lambda k: k[1])
        if path:
            my_path = set()
            current = visited[((x, y), equip)]
            while current != None:
                # print(current)
                my_path.add(current[0])
                current = visited[current]

    j = 0
    for row in map:
        i = 0
        for col in row:
            if (i, j) == (x, y):
                print(ansi_red + "X" + ansi_clear, end="")
            elif (i, j) == target:
                print(ansi_green + "T" + ansi_clear, end="")
            elif path and (i, j) in my_path:
                print(ansi_red + draw[col] + ansi_clear, end="")
            elif visited and (i, j) in l:
                print(ansi_yellow + draw[col] + ansi_clear, end="")
            else:
                print(draw[col], end="")
            i += 1
        j += 1
        if j <= max_y[1]:
            print()
        if j == max_y[1]+1:
            break

    # print over map to see the grid being explored by the a star search
    if backtrack:
        print(f"\033[{max_y[1]+1}A")
    else:
        print()


def mh(x, y, target):
    # Find manhatten distance
    return abs(x-target[0]) + abs(y-target[1])


def part2(data):
    depth = 4080
    target = (14, 785)
    chosen_grid_size_y = 800
    chosen_grid_size_x = 50
    mouth = (0, 0)

    # Create a grid of the risk levels in each cell
    risk_total, risk_map = create_maps(
        chosen_grid_size_x, chosen_grid_size_y, depth, target)

    # Set up for A* search
    torch = "torch"
    gear = "climbing gear"
    neither = "neither"
    type_to_equip = {
        0: set([torch, gear]),
        1: set([gear, neither]),
        2: set([torch, neither])
    }
    came_from = {}
    cost_so_far = {}
    came_from[(mouth, torch)] = None
    cost_so_far[(mouth, torch)] = 0

    q = PriorityQueue()
    q.put((0, (mouth, torch)))
    while not q.empty():
        p, ((x, y), equip) = q.get()

        # print_map(risk_map, x, y, target, came_from, equip)
        if (x, y) == target and equip == torch:
            break

        cells = get_adjacent_cells(
            x, y, chosen_grid_size_x, chosen_grid_size_y)

        # Risk level of current cell
        c = risk_map[y][x]
        for (i, j) in cells:
            # Risk level of next cell
            t = risk_map[j][i]
            h = mh(i, j, target)

            # Only move to a cell if the current equipment allows it
            # or the current equipment can be changed (another equipment that is valid in current cell) to allow it
            for e in type_to_equip[c]:
                if e in type_to_equip[t]:
                    new_cost = cost_so_far[((x, y), equip)] + 1
                    if e != equip:
                        new_cost += 7

                    if ((i, j), e) not in cost_so_far or new_cost < cost_so_far[((i, j), e)]:
                        came_from[((i, j), e)] = ((x, y), equip)
                        cost_so_far[((i, j), e)] = new_cost
                        priority = new_cost + h
                        q.put((priority, ((i, j), e)))

    # print_map(risk_map, x, y, target, came_from,
    #           torch, backtrack=False, path=True)
    return cost_so_far[(target, torch)]
