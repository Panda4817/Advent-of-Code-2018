from copy import deepcopy

def part1(data: str):
    string: list[str] = list(data)
    while True:
        length = len(string)
        removed = False
        for i in range(length-1):
            if (string[i] == string[i + 1].upper() or string[i] == string[i + 1].lower()) and string[i] != string[i + 1]:
                string.pop(i)
                string.pop(i)
                removed = True
                for j in range(i-1, -1, -1):
                    if j == len(string) - 1:
                        break
                    if (string[j] == string[j + 1].upper() or string[j] == string[j + 1].lower()) and string[j] != string[j + 1]:
                        string.pop(j)
                        string.pop(j)
                    else:
                        break
                break
        

        if removed:
            continue

        break
    return len(string)


def part2(data: str):
    letters = "abcdefghijklmnopqrstuvwxyz"
    shortest_length = len(data)
    for l in letters:
        if l not in data and l.upper() not in data:
            continue
        cp = data.replace(l, '').replace(l.upper(), '')
        n = part1(cp)
        if n < shortest_length:
            shortest_length = n

    return shortest_length
