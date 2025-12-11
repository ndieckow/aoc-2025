from dataclasses import dataclass
from collections import defaultdict
from bisect import bisect_left, bisect_right
from time import time

start_time = time()

@dataclass(frozen=True)
class Vec2:
    r: int
    c: int

    def __add__(self, o):
        return Vec2(self.r + o.r, self.c + o.c)

    def __sub__(self, o):
        return Vec2(self.r - o.r, self.c - o.c)

inp = open("09.in").read().splitlines()

points = []
nbs = defaultdict(list)
for line in inp:
    p = tuple(int(x) for x in line.split(','))
    if points:
        nbs[p].append(points[-1])
        nbs[points[-1]].append(p)
    points.append(p)
nbs[points[-1]].append(points[0])
nbs[points[0]] = [points[-1], nbs[points[0]][0]]

#points_sorted_x = sorted(points)
#points_sorted_y = sorted(points, key=lambda x: x[1])

def area(p, q):
    return (abs(p[0] - q[0]) + 1) * (abs(p[1] - q[1]) + 1)

def dir(p, q):
    return sign(q[0] - p[0]), sign(q[1] - p[1])

def sign(x):
    return (1 if x > 0 else -1) if x != 0 else 0

def checky(pad, pbd, qd):
    if pad == (-1,0) and pbd == (0,1) and qd == (1,1):
        return False
    if pad == (0,-1) and pbd == (-1,0) and qd == (-1,1):
        return False
    if pad == (1,0) and pbd == (0,-1) and qd == (-1,-1):
        return False
    if pad == (0,1) and pbd == (1,0) and qd == (1,-1):
        return False
    
    if pad == (0,-1) and pbd == (1,0) and qd != (1,1):
        return False
    if pad == (1,0) and pbd == (0,1) and qd != (-1,1):
        return False
    if pad == (0,1) and pbd == (-1,0) and qd != (-1,-1):
        return False
    if pad == (-1,0) and pbd == (0,-1) and qd != (1,-1):
        return False

    return True

maxarea = 0

for i,p in enumerate(points):
    a, b = nbs[p]
    pad = dir(a, p) # (0,-1)
    pbd = dir(p, b) # (1,0)

    for q in points[i+1:]:
        qd = dir(p, q)
        pd = dir(q, p)

        qa, qb = nbs[q]
        qad = dir(qa, q)
        qbd = dir(q, qb)

        # check validity
        if not (checky(pad, pbd, qd) and checky(qad, qbd, pd)):
            continue

        flag = False
        min_x, max_x = min(p[0],q[0]), max(p[0],q[0])
        min_y, max_y = min(p[1],q[1]), max(p[1],q[1])

        #print(p, q, disruptors)
        for a,b in list(zip(points,points[1:])) + [(points[-1],points[0])]:
            if a[0] == b[0]:  # vertical line
                c, d = (a, b) if a[1] < b[1] else (b, a)
                if min_x < a[0] < max_x and (c[1] <= min_y and d[1] > min_y or min_y <= c[1] < max_y or c[1] < max_y and d[1] >= max_y):
                    flag = True
                    break
            else:  # horizontal line
                c, d = (a, b) if a[0] < b[0] else (b, a)
                if min_y < a[1] < max_y and (c[0] <= min_x and d[0] > min_x or min_x <= c[0] < max_x or c[0] < max_x and d[0] >= max_x):
                    flag = True
                    break
        if flag:
            continue
        maxarea = max(maxarea, area(p, q))
print(maxarea)
print(time() - start_time)

# Naive: 14 s
# With checky-checky: 8 s