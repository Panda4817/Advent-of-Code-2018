def process_data(data):
    coords = [tuple(int(i) for i in lines.split(", ")) for lines in data.split("\n")]
    coords.sort(key=lambda x: x[1], reverse=True)
    rows = coords[0][1] + 1
    coords.sort(key=lambda x: x[0], reverse=True)
    cols = coords[0][0] + 1
    return coords, rows, cols

def isInfinite(x, y, rows, cols):
    if x == 0 or x == cols - 1:
        return True
    if y == 0 or y == rows - 1:
        return True

def part1(data):
    coords, rows, cols = process_data(data)
    areas = {c: {"area": 1, "coords": [c]} for c in coords}
    for y in range(rows):
        for x in range(cols):
            if (x, y) in areas:
                continue
            mh = {}
            for coord in coords:
                dist = abs(x - coord[0]) + abs(y - coord[1])
                mh[coord] = dist
            sorted_list = list(mh.items())
            sorted_list.sort(key=lambda i: i[1])
            if sorted_list[0][1] != sorted_list[1][1]:
                areas[sorted_list[0][0]]["area"] += 1
                areas[sorted_list[0][0]]["coords"].append((x, y))

    results = {}           
    for k, v in areas.items():
        for (x, y) in v["coords"]:
            if isInfinite(x, y, rows, cols):
                break
        else:
            results[k] = v["area"]

    sorted_areas = list(results.items())
    sorted_areas.sort(key=lambda i: i[1], reverse=True)

    return sorted_areas[0][1]


def part2(data):
    desired_total_dist = 10000
    coords, rows, cols = process_data(data)
    possible_coords = []
    for y in range(rows):
        for x in range(cols):
            total_dist = 0
            for coord in coords:
                dist = abs(x - coord[0]) + abs(y - coord[1])
                total_dist += dist
                
            if total_dist < desired_total_dist:
                possible_coords.append((x, y))
    
    return len(possible_coords)
