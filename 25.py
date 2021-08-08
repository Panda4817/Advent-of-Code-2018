def process_data(data):
    lines = data.split("\n")
    points = set()
    for line in lines:
        numbers = tuple(int(i) for i in line.split(","))
        points.add(numbers)
    return points


def is_mh_three_or_less(a, b):
    mh = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])
    if mh <= 3:
        return True

    return False


def recurse_through_stars(current_set, first, all_stars, done):
    for star in all_stars:
        if star in done:
            continue

        if is_mh_three_or_less(first, star):
            current_set.add(star)
            done.add(star)
            current_set, done = recurse_through_stars(
                current_set, star, all_stars, done
            )

    return current_set, done


def part1(data):
    points = process_data(data)
    constellations = []
    done = set()
    for point in points:
        if point in done:
            continue
        single_constellation = set()
        single_constellation.add(point)
        done.add(point)
        single_constellation, done = recurse_through_stars(
            single_constellation, point, points, done
        )
        constellations.append(single_constellation)

    return len(constellations)
