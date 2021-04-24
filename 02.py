
def part1(data):
    ids = data.split("\n")
    two = 0
    three = 0
    for id in ids:
        done  = ''
        two_done = False
        three_done = False
        for char in id:
            if two_done and three_done:
                break
            if char in done:
                continue
            done += char
            n = id.count(char)
            if n == 2 and not two_done:
                two += 1
                two_done = True
            elif n == 3 and not three_done:
                three += 1
                three_done = True
    
    return two * three

def part2(data):
    ids = data.split("\n")

    for id in ids:
        found = None
        for id2 in ids:
            if id2 == id:
                continue
            diff = [i for i in range(len(id)) if id[i] != id2[i]]
            if len(diff) == 1:
                found = id2
                break
        if found:
            break
        l = []
        
    res = ''
    for a, b in zip(id, found):
        if a == b:
            res += a
    return res

