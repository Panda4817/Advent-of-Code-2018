from collections import deque
from typing import List


def print_traversed(doors, max_doors, current, instructions=None):
    string = ""
    if instructions:
        string += "".join(instructions)
    print(string, current, doors, max_doors)


def create_door_map(data):

    current_room_stack = [(0, 0)]
    visited = [current_room_stack]
    doors_stack = [0]
    instructions = []
    directions = {
        "E": (1, 0),
        "W": (-1, 0),
        "N": (0, -1),
        "S": (0, 1)
    }

    # Part 2
    all_door_counts = {}
    # Part 1
    max_doors = 0

    q = deque(list(data)[1:-1])  # Stack

    while q:
        d = q.popleft()
        instructions.append(d)
        # print_traversed(doors, max_doors, current, instructions)
        if d == "(":
            current_room_stack.append(current_room_stack[-1])
            doors_stack.append(doors_stack[-1])
            continue
        elif d == "|":
            coord = current_room_stack.pop()
            door = doors_stack.pop()

            # Part 2
            if tuple(coord) not in all_door_counts:
                all_door_counts[tuple(coord)] = door

            # Part 1
            max_doors = max(door, max_doors)

            current_room_stack.append(current_room_stack[-1])
            doors_stack.append(doors_stack[-1])
            continue
        elif d == ")":
            coord = current_room_stack.pop()
            door = doors_stack.pop()

            # Part 2
            if tuple(coord) not in all_door_counts:
                all_door_counts[tuple(coord)] = door

            # Part 1
            max_doors = max(door, max_doors)

            continue

        coord = current_room_stack.pop()
        door = doors_stack.pop()

        i, j = directions[d]
        x, y = coord[0] + i, coord[1] + j
        current_room_stack.append((x, y))

        if (x, y) in visited:
            doors_stack.append(door)
            continue

        door += 1
        doors_stack.append(door)
        visited.append((x, y))

        # Part 1
        max_doors = max(door, max_doors)

        # Part 2
        all_door_counts[(x, y)] = door

    # Part 2
    rooms_with_1000_doors = 0
    for room in all_door_counts:
        if all_door_counts[room] >= 1000:
            rooms_with_1000_doors += 1

    return max_doors, rooms_with_1000_doors


def part1(data):
    max_doors, part2 = create_door_map(data)
    return max_doors


def part2(data):
    max_doors, part2 = create_door_map(data)
    return part2
