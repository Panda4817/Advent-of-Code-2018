def process_data(data: str):
    lst = data.split("\n")
    new_list = []
    for line in lst:
        text = line[19:]
        year = int(line[1:5])
        month = int(line[6:8])
        day = int(line[9:11])
        hour = int(line[12:14])
        minute = int(line[15:17])
        new_list.append((year, month, day, hour, minute, text))
    new_list.sort(key=lambda x: x[4])
    new_list.sort(key=lambda x: x[3])
    new_list.sort(key=lambda x: x[2])
    new_list.sort(key=lambda x: x[1])
    new_list.sort(key=lambda x: x[0])
    return new_list


def part1(data):
    processed_data = process_data(data)
    guards = {}
    current_guard = 0
    fell_asleep = 0
    for p in processed_data:
        if "Guard" in p[5]:
            num = int(p[5].split()[1][1:])
            if num not in guards:
                guards[num] = {"total": 0, "minutes": []}
            current_guard = num

        if p[5] == "falls asleep":
            fell_asleep = p[4]

        if p[5] == "wakes up":
            guards[current_guard]["total"] += p[4] - fell_asleep
            for i in range(fell_asleep, p[4]):
                guards[current_guard]["minutes"].append(i)
    sorted_dict = list(guards.items())
    sorted_dict.sort(key=lambda x: x[1]["total"], reverse=True)
    chosen_guard = sorted_dict[0]
    minutes_frequency = {}
    for m in chosen_guard[1]["minutes"]:
        minutes_frequency[m] = minutes_frequency.get(m, 0) + 1
    max_minute = max(minutes_frequency.items(), key=lambda x: x[1])[0]
    return chosen_guard[0] * max_minute


def part2(data):
    processed_data = process_data(data)
    guards = {}
    current_guard = 0
    fell_asleep = 0
    for p in processed_data:
        if "Guard" in p[5]:
            num = int(p[5].split()[1][1:])
            if num not in guards:
                guards[num] = {x: 0 for x in range(0, 60)}
            current_guard = num

        if p[5] == "falls asleep":
            fell_asleep = p[4]

        if p[5] == "wakes up":
            for i in range(fell_asleep, p[4]):
                guards[current_guard][i] = guards[current_guard].get(i, 0) + 1

    highest_freq = 0
    chosen_guard = 0
    chosen_minute = 0
    for k, v in guards.items():
        values = list(v.items())
        values.sort(key=lambda x: x[1], reverse=True)
        if values[0][1] > highest_freq:
            highest_freq = values[0][1]
            chosen_guard = k
            chosen_minute = values[0][0]

    return chosen_minute * chosen_guard
