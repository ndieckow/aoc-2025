from collections import defaultdict

lines = open("07.in").read().splitlines()
R, C = len(lines), len(lines[0])

beams = set()
for c in range(C):
    if lines[0][c] == 'S':
        sc = c
        beams.add(c)
        break

ans = 0
for r in range(1, R):
    new_beams = set()
    for c in beams:
        if lines[r][c] == '.':
            new_beams.add(c)
        else:
            ans += 1
            new_beams.update([c-1, c+1])
    beams = new_beams
print("Part 1:", ans)

# PART 2
ways = defaultdict(int)
ways[2, sc] = 1
def dp(r, c):
    if (r, c) in ways:
        return ways[r, c]
    # walk up
    ret = 0
    rr = r-1
    while rr >= 0:
        for dc in [-1, 1]:
            if lines[rr][c+dc] == '^':
                ret += dp(rr, c+dc)
        if lines[rr][c] == '^':
            break
        rr -= 1
    ways[r, c] = ret
    return ways[r, c]

ans2 = 0
for r in range(R):
    for c in range(C):
        if lines[r][c] == '^':
            ans2 += dp(r, c)
print("Part 2:", ans2 + 1)