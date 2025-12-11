from collections import deque
from math import inf
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

inp = open("10.in").read().splitlines()

ans = 0
ans2 = 0
for line in inp:
    args = line.split()
    dia, jolt = args[0], args[-1]
    buttons = args[1:-1]
    buttons = [tuple(int(y) for y in x[1:-1].split(',')) for x in buttons]

    dia = dia[1:-1]
    
    # BFS
    s = tuple('.' * len(dia))
    Q = deque([(s, 0)])
    seen = set([s])
    while Q:
        v, k = Q.popleft()
        if ''.join(v) == dia:
            ans += k
            break
        for b in buttons:
            w = list(v)
            for i in b:
                w[i] = '#' if w[i] == '.' else '.'
            w = tuple(w)
            if w in seen:
                continue
            seen.add(w)
            Q.append((w, k+1))
    
    # Ax = b
    jolt = [int(x) for x in jolt[1:-1].split(',')]
    b = np.array(jolt)
    A = np.zeros((len(jolt), len(buttons)))
    for i,but in enumerate(buttons):
        A[:,i] = np.array([1 if j in but else 0 for j in range(len(jolt))])
    c = np.ones(A.shape[1])
    constraints = LinearConstraint(A, lb=b, ub=b)
    integrality = np.ones(A.shape[1])
    bounds = Bounds(lb=0, ub=np.inf)
    res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    ans2 += int(res.x.sum())


print(ans)
print(ans2)