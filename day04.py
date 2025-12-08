from itertools import product
from copy import deepcopy

grid = open("04.in").read().splitlines()
R = len(grid)
C = len(grid[0])

ans = 0
while True:
    loc_ans = 0
    newgrid = [list(x) for x in grid]
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '.':
                continue
            nbs = 0
            for dr,dc in product([-1,0,1], repeat=2):
                if dr == dc == 0:
                    continue
                if not 0 <= (r+dr) < R or not 0 <= (c+dc) < C:
                    continue
                nbs += (grid[r+dr][c+dc] == '@')
            if nbs < 4:
                loc_ans += 1
                newgrid[r][c] = '.'
    if loc_ans == 0:
        break
    if ans == 0:
        print("Part 1:", loc_ans)
    ans += loc_ans
    grid = newgrid

print("Part 2:", ans)