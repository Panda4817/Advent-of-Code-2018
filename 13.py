from copy import deepcopy


def get_direction_from_symbol(symbol):
    """
    Return what to add to (x, y) to move in that direction and what to replace that cart with to complete the track map.
    """
    if symbol == ">":
        return (1, 0), "-"
    elif symbol == "<":
        return (-1, 0), "-"
    elif symbol == "v":
        return (0, 1), "|"
    else:
        return (0, -1), "|"


def corner_check(cart, grid):
    """Check if the current coordinate is a corner, if so minecart needs to turn"""
    next_dir = {
        (1, 0): {"\\": (0, 1), "/": (0, -1)},
        (-1, 0): {"\\": (0, -1), "/": (0, 1)},
        (0, 1): {"\\": (1, 0), "/": (-1, 0)},
        (0, -1): {"\\": (-1, 0), "/": (1, 0)}
    }
    x = cart["coord"][0]
    y = cart["coord"][1]
    corner = grid[y][x]
    if corner != "\\" and corner != "/":
        return cart

    current = cart["dir"]
    cart["dir"] = next_dir[current][corner]
    return cart


def turn_check(cart, grid):
    """Check if the current coordinate is an intersection, if so minecart needs to gor left, straight on or turn right"""
    next_turn = {
        1:  2,
        2:  3,
        3:  1
    }
    turns = {
        1: {(1, 0): (0, -1), (-1, 0): (0, 1), (0, 1): (1, 0), (0, -1): (-1, 0)},
        2: {(1, 0): (1, 0), (-1, 0): (-1, 0), (0, 1): (0, 1), (0, -1): (0, -1)},
        3: {(1, 0): (0, 1), (-1, 0): (0, -1), (0, 1): (-1, 0), (0, -1): (1, 0)}
    }
    x = cart["coord"][0]
    y = cart["coord"][1]
    intersection = grid[y][x]
    if intersection != "+":
        return cart

    turn = cart["turn"]
    current_dir = cart["dir"]
    current_turn = cart["turn"]
    cart["dir"] = turns[current_turn][current_dir]
    cart["turn"] = next_turn[turn]
    return cart


def check_collision(carts, cart, cart_num):
    """Check if the current minecart's new coordinate collides with another cart"""
    for k, v in carts.items():
        if k == cart_num:
            continue
        if v["coord"] == cart["coord"]:
            return (v["coord"], k)

    return False


def process_data(data):
    """Retrieve the data and return a grid and a cart hash map"""
    grid = [list(l) for l in data.split("\n")]
    carts = {}
    cart = 1
    cart_symbols = [">", "<", "^", "v"]
    grid_copy = deepcopy(grid)
    for r, y in zip(grid_copy, range(len(grid_copy))):
        for c, x in zip(r, range(len(r))):
            if c in cart_symbols:
                d, replace_with = get_direction_from_symbol(c)
                carts[cart] = {"dir": d, "coord": [x, y], "turn": 1}
                grid[y][x] = replace_with
                cart += 1
    return grid, carts


def print_grid(grid, carts):
    """For debugging"""
    for r, y in zip(grid, range(len(grid))):
        for c, x in zip(r, range(len(r))):
            for k, v in carts.items():
                if [x, y] == v["coord"]:
                    print("c", end="")
                    break
            else:
                print(c, end="")
        print()


def part1(data):
    """Returns coordinate of first minecarts colliding"""
    grid, carts = process_data(data)

    while True:
        first_collision = False
        for k, v in carts.items():
            x = v["coord"][0]
            y = v["coord"][1]
            carts[k]["coord"] = [x + v["dir"][0], y + v["dir"][1]]
            carts[k] = corner_check(carts[k], grid)
            carts[k] = turn_check(carts[k], grid)
            ans = check_collision(carts, carts[k], k)
            if ans:
                first_collision = True
                break
        if first_collision:
            break

        carts = dict(sorted(carts.items(), key=lambda v: v[1]["coord"][0]))
        carts = dict(sorted(carts.items(), key=lambda v: v[1]["coord"][1]))

    return ans


def part2(data):
    """Returns the last minecart left on the track"""
    grid, carts = process_data(data)
    while True:
        to_remove = set()
        for k, v in carts.items():
            x = v["coord"][0]
            y = v["coord"][1]
            carts[k]["coord"] = [x + v["dir"][0], y + v["dir"][1]]
            carts[k] = corner_check(carts[k], grid)
            carts[k] = turn_check(carts[k], grid)
            ans = check_collision(carts, carts[k], k)
            if ans:
                to_remove.add(k)
                to_remove.add(ans[1])

        for k in to_remove:
            del carts[k]

        carts = dict(sorted(carts.items(), key=lambda v: v[1]["coord"][0]))
        carts = dict(sorted(carts.items(), key=lambda v: v[1]["coord"][1]))

        if len(carts) == 1:
            break

    return carts
