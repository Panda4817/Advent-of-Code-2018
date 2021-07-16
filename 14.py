def print_recipes(scores, a, b, scores_length):
    for i in range(scores_length):
        if i == a:
            print("(" + str(scores[i]) + ")", end="")
        elif i == b:
            print("[" + str(scores[i]) + "]", end="")
        else:
            print(scores[i], end="")
    print()


def next_recipe(scores, current, scores_length):
    rotate_by = 1 + scores[current] + current
    return rotate_by % scores_length
    # i = current
    # for r in range(rotate_by):
    #     i += 1
    #     if i >= scores_length:
    #         i = 0
    # return i


def next_scores(scores, a, b, scores_length):
    total = sum((scores[a], scores[b]))
    digits = [int(i) for i in str(total)]
    scores_length += len(digits)
    scores.extend(digits)
    a = next_recipe(scores, a, scores_length)
    b = next_recipe(scores, b, scores_length)

    return scores, scores_length, a, b


def part1(data):
    scores = [3, 7]
    scores_length = 2
    recipes = int(data)
    a = 0
    b = 1

    while scores_length <= recipes + 10:
        scores, scores_length, a, b = next_scores(scores, a, b, scores_length)

    return "".join([str(i) for i in scores[recipes:recipes + 10]])


def check_for_final(scores, final, final_length, index, scores_length):
    for i in range(index, scores_length - final_length):
        if scores[i:i+final_length] == final:
            return scores[:i]

    return False


def part2(data):
    scores = [3, 7]
    final = [int(i) for i in data]
    final_length = len(final)
    a = 0
    b = 1
    index = 0
    ticks = 0
    scores_length = 2
    while True:
        ans = check_for_final(
            scores, final, final_length, index, scores_length)
        if ans:
            break

        scores, scores_length, a, b = next_scores(scores, a, b, scores_length)

        ticks += 1
        if ticks == final_length + 1:
            index += 1
            while scores[index] != final[0]:
                index += 1
                if index == scores_length:
                    break
            ticks = 0

    return len(ans)
