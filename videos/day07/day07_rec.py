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
print("Part 1:", ans)


from collections import defaultdict

dp = defaultdict(int)
dp[2, sc] = 1
ans2 = 0
for r in range(R):
    for c in range(C):
        if grid[r][c] != '^':
            continue
        for cc in [-1, 1]:
            for rr in range(1, R-r):
                if grid[r+rr][c+cc] == '^':
                    dp[r+rr][c+cc] += dp[r,c]
                    break
        ans2 += dp[r, c]
print("Part 2:", ans2 + 1)