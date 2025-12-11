grid = open("07.in").read().splitlines()
R, C = len(grid), len(grid[0])

sc = C // 2
beams = set([sc])

ans = 0
for r in range(R):
    new_beams = set()
    for c in beams:
        if grid[r][c] == '^':
            ans += 1
            new_beams.update([c-1, c+1])
        else:
            new_beams.add(c)
    beams = new_beams
print(ans)