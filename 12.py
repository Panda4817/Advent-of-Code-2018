from blist import blist


def get_state(data):
    lst = data.split("\n")
    state = [0 if l == "." else 1 for l in lst[0].split()[2]]
    index = set([i for i in range(len(state)) if state[i] == 1])
    rules_with_plant = []
    rules_without_plant = []
    for line in lst[2:]:
        parts = line.split(" => ")
        if parts[1] == ".":
            continue
        rule = []
        x = -2
        for r in parts[0]:
            if r == "#":
                rule.append(x)
            x += 1
        if 0 in rule:
            rules_with_plant.append(rule)
        else:
            rules_without_plant.append(rule)
    return index, blist(rules_with_plant), blist(rules_without_plant)


def print_gen(state, min_index, max_index, gen):
    print(gen, end=" ")
    for i in range(min_index - 2, max_index + 3):
        if i in state:
            print("#", end="")
        else:
            print(".", end="")
    print()


def part1(data):
    state, rules_with, rules_without = get_state(data)
    generation = 0

    # Part 1 - 20 generations (no need to to do any part 2 stuff)
    total_gens = 102  # after this number, the pattern of plants shift by 1

    # Part 2 - 50000000000
    gens = 50000000000

    min_index = min(state)
    max_index = max(state)
    # print_gen(state, min_index, max_index, generation)

    while generation != total_gens:
        new_state = set([])
        not_in_state = set(range(min_index - 2, max_index + 3)) - state
        for i in state:
            for rule in rules_with:
                for c in [-2, -1, 0, 1, 2]:
                    n = i + c
                    if (c not in rule and n in state) or (c in rule and n not in state):
                        break
                else:
                    new_state.add(i)
                    break

        for i in not_in_state:
            for rule in rules_without:
                for c in [-2, -1, 1, 2]:
                    n = i + c
                    if (c not in rule and n in state) or (c in rule and n not in state):
                        break

                else:
                    new_state.add(i)
                    if i < min_index:
                        min_index = i
                    if i > max_index:
                        max_index = i
                    break

        state = new_state
        generation += 1
        # print_gen(state, min_index, max_index, generation)

    # Part 2 logic
    left_over = gens - total_gens
    final_state = set()
    for i in state:
        final_state.add(i + left_over)

    return sum(final_state)  # Part 2, Part 1 - sum(state)
