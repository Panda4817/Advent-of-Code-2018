from blist import blist


def process_data(data):
    lines = data.split("\n")
    stars = blist([])
    velocities = blist([])
    for line in lines:
        # test
        # position_string = line[10:16]
        # velocity_string = line[28:-1]
        position_string = line[10:24]
        velocity_string = line[36:-1]
        star = [int(x) for x in position_string.split(", ")]
        speed = [int(x) for x in velocity_string.split(", ")]
        stars.append(star)
        velocities.append(speed)

    return stars, velocities


def prepare_grid(stars):
    # Prepare into a grid
    highest_x = 0
    lowest_x = 0
    lowest_y = 0
    highest_y = 0
    for star in stars:
        if star[0] > highest_x:
            highest_x = star[0]

        if star[1] > highest_y:
            highest_y = star[1]

        if star[0] < lowest_x:
            lowest_x = star[0]

        if star[1] < lowest_y:
            lowest_y = star[1]

    cols = abs(lowest_x) + highest_x + 1
    rows = abs(lowest_y) + highest_y + 1
    index = 0
    match_up_x = {}
    match_up_y = {}
    for i in range(lowest_x, highest_x + 1):
        match_up_x[i] = index
        index += 1
    index = 0

    for i in range(lowest_y, highest_y + 1):
        match_up_y[i] = index
        index += 1

    for i in range(len(stars)):
        stars[i][0] = match_up_x[stars[i][0]]
        stars[i][1] = match_up_y[stars[i][1]]

    return cols, rows, stars


def isAligned(stars):
    row = [-1, -1, -1, 0, 0, 1, 1, 1]
    col = [-1, 0, 1, -1, 1, -1, 0, 1]
    for star in stars:
        aligned = False
        for i in range(8):
            y = star[1] + row[i]
            x = star[0] + col[i]
            if [x, y] in stars:
                aligned = True
                break
        if not aligned:
            return False

    return True


def print_stars(stars):
    cols, rows, stars_grid = prepare_grid(stars)
    for r in range(rows):
        print_line = False
        for star in stars_grid:
            if r in star:
                print_line = True
                break

        if print_line:
            for c in range(cols):
                if [c, r] not in stars_grid:
                    print(" ", end="")
                else:
                    print("#", end="")

            print()
    return


def part1(data):
    stars, speeds = process_data(data)
    seconds = 0
    number = len(stars)
    while isAligned(stars) == False:
        seconds += 1
        for n in range(number):
            temp = [stars[n][0] + speeds[n][0], stars[n][1] + speeds[n][1]]
            stars[n][0] = temp[0]
            stars[n][1] = temp[1]
    print_stars(stars)
    return seconds
