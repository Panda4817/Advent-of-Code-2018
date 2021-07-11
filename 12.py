
def get_state(data):
    lst = data.split("\n")
    state = [0 if l == "." else 1 for l in lst[0].split()[2]]
    index = set([i for i in range(len(state)) if state[i] == 1])
    rules = []
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
        rules.append(rule)
    return index, tuple(rules)


def part1(data):
    state, rules = get_state(data)
    generation = 0
    total_gens = 20  # 50000000000
    while generation != total_gens:
        new_state = set()
        min_index = min(state)
        max_index = max(state)
        for i in range(min_index - 2, max_index + 3):
            for rule in rules:
                for c in [-2, -1, 0, 1, 2]:
                    n = i + c
                    if (c not in rule and n in state) or (c in rule and n not in state):
                        break

                else:
                    new_state.add(i)
                    break

        state = new_state
        generation += 1
    return sum(state)
