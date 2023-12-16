def calculate_reflection(p1, p2, y=-1, smudge=False):
    if e and len([u for u in range(len(d[e])) if d[e][u] != d[e - 1][u]]) < 2:
        for i in range(e, len(d) + 1):
            y += 2
            if i - y < 0 or i == len(d):
                if smudge: p2 += e * multiplier
                else:      p1 += e * multiplier
                break
            if d[i] != d[i - y]:
                if not smudge and len([u for u in range(len(d[i])) if d[i][u] != d[i - y][u]]) == 1:
                    smudge = True
                else: break
    return p1, p2

with open("r13_input.txt", "r") as file:
    data = file.read().split("\n\n")
    p1 = p2 = 0
    for grid in data:
        h = [*map(list, grid.split())]
        v = [*map(list, zip(*h))]
        for d, multiplier in ((h, 100), (v, 1)):
            for e, x in enumerate(d):
                p1, p2 = calculate_reflection(p1, p2)
    print(p1, p2)