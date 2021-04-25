start = 'start'
end = 'end'
def process_data(data):
    grid = []
    for i in range(1000):
        grid.append([0] * 1000)
    rectangles = {}
    for line in data.split("\n"):
        l = line.split()
        s = [int(i) if ':' not in i else int(i[0:-1]) for i in l[2].split(",")]
        s.reverse()
        e = [int(i) for i in l[3].split("x")]
        e.reverse()
        e[0] = s[0] + e[0]
        e[1] = s[1] + e[1]
        rectangles[int(l[0][1:])] = {start: s, end: e}
    return grid, rectangles

def part1(data):
    grid, rectangles = process_data(data)
    overlap = 0
    for k, v in rectangles.items():
        for r in range(v[start][0], v[end][0]):
            for c in range(v[start][1], v[end][1]):
                if grid[r][c] > 0:
                    overlap += 1
                    grid[r][c] = -1
                    continue
                elif grid[r][c] < 0:
                    continue
                grid[r][c] = k
    
    return overlap

def part2(data):
    grid, rectangles = process_data(data)
    claims = set(rectangles.keys())
    for k, v in rectangles.items():
        for r in range(v[start][0], v[end][0]):
            for c in range(v[start][1], v[end][1]):
                if grid[r][c] > 0 or grid[r][c] < 0:
                    if grid[r][c] in claims:
                        claims.remove(grid[r][c])
                    if k in claims:
                        claims.remove(k)
                    grid[r][c] = -1
                    continue
                grid[r][c] = k
    
    return claims
                
                
        

