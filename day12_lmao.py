import numpy as np
from collections import deque

lines = open("12.in").read().splitlines()

def f(x):
    if x == '.': return 0
    elif x == '#': return 1

shapes = [np.array([list(map(f, s)) for s in lines[5*i+1:5*i+4]]) for i in range(6)]
regions = lines[30:]

ans = 0
for i,region in enumerate(regions):
    size, pres = region.split(':')
    size = [int(x) for x in size.split('x')]
    pres = [int(x) for x in pres.split()]

    n_pres = sum(shapes[i].sum() * p for i,p in enumerate(pres))
    if n_pres * 1.3 < size[0]*size[1]:
        ans += 1
print(ans)