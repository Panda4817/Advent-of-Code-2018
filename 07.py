from typing import OrderedDict
import networkx as nx


def process_data(data):
    prerequisites = OrderedDict()
    list_data = []
    for line in data:
        sentence = line.split()
        first = sentence[1]
        second = sentence[7]
        list_data.append((first, second))
        if second in prerequisites and first not in prerequisites[second]:
            prerequisites[second].append(first)
        else:
            prerequisites[second] = [first]
        prerequisites[second].sort()
    sorted = list(prerequisites.items())
    sorted.sort(
        key=lambda x: x[0])
    prerequisites = {x[0]: x[1] for x in sorted}
    return prerequisites, list_data

# My own implementation of a lexicographical topological sort
# def recurse(dict, l, temp: list = []):
#     if l not in dict:
#         if l not in temp:
#             temp.append(l)
#         return temp

#     for p in dict[l]:
#         recurse(dict, p, temp)

#     if l not in temp:
#         temp.append(l)
#     return temp


def part1(data: str):
    prerequisites, edges = process_data(data.split("\n"))
    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    # hashmap of letter and its prerequisite letters for part 2 and own implementation of the sort
    return "".join(nx.lexicographical_topological_sort(G)), prerequisites

    # My own implementation of a lexicographical topological sort
    # instructions = []
    # letters_set = set(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")) - set(instructions)
    # letters_list = list(letters_set)
    # letters_list.sort()
    # done = set()
    # while True:
    #     # Go through the letters and recurse through until all prerequisites are placed
    #     l = letters_list.pop(0)
    #     if l in done:
    #         continue
    #     temp = recurse(prerequisites, l, [])
    #     for t in temp:
    #         if t not in done:
    #             instructions.append(t)
    #             done.add(t)

    #     # Add one more letter if possible (more than one goes out of order)
    #     for letter in letters_list:
    #         if letter in done:
    #             continue
    #         if letter not in prerequisites:
    #             instructions.append(letter)
    #             done.add(letter)
    #             continue
    #         count = 0
    #         for p in prerequisites[letter]:
    #             if p in instructions:
    #                 count += 1
    #         if count == len(prerequisites[letter]):
    #             instructions.append(letter)
    #             done.add(letter)
    #             break

    #     if len(instructions) == 26:
    #         break

    # return "".join(instructions)


def part2(data):
    steps_string, prequisites = part1(data)
    steps = list(steps_string)
    workers = {x: {"start": None, "l": None, "end": None} for x in range(1, 6)}
    available_workers = [x for x in range(1, 6)]
    done = set()
    time = 60
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    total_time = -1
    while True:
        # Increase seconds
        total_time += 1

        # Check if worksers are done and reset them
        for k, v in workers.items():
            if v["start"] == None:
                continue
            if total_time == v["end"]:
                available_workers.append(k)
                done.add(workers[k]["l"])
                workers[k]["start"] = None
                workers[k]["l"] = None
                workers[k]["end"] = None

        # Check if all steps are completed
        if len(done) == 26:
            break

        # Assign workers if available
        while available_workers:
            available_letter = False
            for i in range(len(steps)):
                if steps[i] not in prequisites:
                    available_letter = True
                    break

                count = 0
                for p in prequisites[steps[i]]:
                    if p in done:
                        count += 1
                if count == len(prequisites[steps[i]]):
                    available_letter = True
                    break

            if available_letter:
                letter = steps.pop(i)
                worker = available_workers.pop(0)
                workers[worker]["start"] = total_time
                workers[worker]["l"] = letter
                letter_time = letters.index(letter) + 1
                workers[worker]["end"] = total_time + time + letter_time
            else:
                break

    return total_time
