from blist import blist


def part1(data):
    # 71657 - part 1
    # 71657 * 100 - part 2
    marbles = 7165700
    players = 476
    circle = blist([0])
    length = 1
    scores = [0 for p in range(players)]
    current_marble_index = 0
    player = 0
    highest_score = 0
    for m in range(1, marbles + 1):
        if m % 23 == 0:
            scores[player] += m
            index = current_marble_index - 7
            if index < 0:
                index = length + index
            scores[player] += circle.pop(index)
            if scores[player] > highest_score:
                highest_score = scores[player]
            length -= 1

        else:

            index = current_marble_index + 2
            if index >= length:
                index = index - length
            circle.insert(index, m)
            length += 1

        current_marble_index = index
        player += 1
        if player >= players:
            player = 0

    return highest_score
