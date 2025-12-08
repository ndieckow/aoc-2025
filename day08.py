from math import sqrt, prod
from collections import Counter

boxes = open("08.in").read().splitlines()
boxes = [tuple(int(x) for x in box.split(',')) for box in boxes]

def sqdist(p, q):
    return sum((p[i] - q[i])**2 for i in range(3))

dist_dict = {}
for i,p in enumerate(boxes):
    for q in boxes[i+1:]:
        pair = frozenset([p, q])
        dist_dict[pair] = sqdist(p, q)
sort_dist = sorted(dist_dict.keys(), key=lambda x: dist_dict[x])

r = {x: x for x in boxes}

def find(p):
    if r[p] == p:
        return p
    r[p] = find(r[p])
    return r[p]

def merge(p, q):
    if find(p) == find(q):
        return False
    r[find(q)] = find(p)
    return True

k = 0
for i,(p, q) in enumerate(sort_dist):
    if merge(p, q):
        k += 1

    if i == 999:
        sz = Counter(find(p) for p in boxes)
        print("Part 1:", prod(sorted(sz.values())[-3:]))

    if k == len(boxes) - 1:
        print("Part 2:", p[0] * q[0])
        break