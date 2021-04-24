
def process_data(data):
    numbers = [int(l) if l[0] == '-' else int(l[1:]) for l in data.split("\n")]
    return numbers

def part1(data):
    numbers = process_data(data)
    freq = 0
    for n in numbers:
        freq += n
    return freq

def part2(data):
    numbers = process_data(data)
    freq = set([0])
    current_freq = 0
    found = False
    while not found:
        for n in numbers:
            current_freq += n
            if current_freq in freq:
                found = True
                break   
            freq.add(current_freq)
    return current_freq
