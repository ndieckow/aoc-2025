from collections import defaultdict
from bisect import bisect_left

inp = open("09.test2").read().splitlines()

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

points_sorted_x = sorted(points)
points_sorted_y = sorted(points, key=lambda x: x[1])

def sign(x):
    return (1 if x > 0 else -1) if x != 0 else 0

def area(p, q):
    return (abs(p[0] - q[0]) + 1) * (abs(p[1] - q[1]) + 1)

"""
def valid(p, q):
    # check for local consistency
    for k in range(2):
        if k == 1:
            p, q = q, p
        flags = [False, False]
        for nb in nbs[p]:
            for i in range(2):
                if sign(q[i] - p[i]) == sign(nb[i] - p[i]):
                    flags[i] = True
        if not all(flags):
            return False
    return True
"""

def within(p, q):
    # check whether a red tile is within the rectangle spanned by p and q
    p, q = (p, q) if p < q else (q, p)
    idx = bisect_left(points_sorted_x, p)
    for i in range(idx, len(points)):
        s = points_sorted_x[i]
        if p[0] < s[0] < q[0] and min(p[1], q[1]) < s[1] < max(p[1], q[1]):
            return True
        if s >= q:
            break
    return False

maxarea = 0

for i,p in enumerate(points):
    for q in points[i+1:]:
        tmp = maxarea
        maxarea = max(maxarea, area(p, q))

print(maxarea)

def dir(p, q):
    return sign(q[0] - p[0]), sign(q[1] - p[1])

def vecsign(p):
    return sign(p[0]), sign(p[1])

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

maxarea3 = 0
for i,p in enumerate(points):
    a, b = nbs[p]
    pad = dir(a, p) # (0,-1)
    pbd = dir(p, b) # (1,0)
    
    overall_best = 0
    cur_best = 0
    underwater_flag = False

    for q in points[i+1:]:
        qd = dir(p, q)
        pd = dir(q, p)

        qa, qb = nbs[q]
        qad = dir(qa, q)
        qbd = dir(q, qb)

        underwater = not checky(pad, pbd, qd)
        print(pad, pbd, qd, q)
        #print(p, q, underwater)
        if underwater:
            if not underwater_flag:
                overall_best = max(cur_best, overall_best)
            cur_best = 0
            underwater_flag = True
            continue
        
        if not checky(qad, qbd, pd):
            #print(p, q, "not checky :(")
            continue
        
        if within(p, q):
            #print(p, q, "something within :(")
            continue
        
        tmp = cur_best
        cur_best = max(cur_best, area(p, q))
        if cur_best != tmp:
            print(p, q, cur_best)
    
    overall_best = max(overall_best, cur_best)
    tmp = maxarea3
    maxarea3 = max(overall_best, maxarea3)
    if tmp != maxarea3:
        print("OBOBOB", p, nbs[p])
print(maxarea3)

for p in points:
    if 17454 < p[0] < 82409 and 14643 < p[1] < 85504:
        print(p)