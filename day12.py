import numpy as np
from collections import deque

lines = open("12.test").read().splitlines()

def f(x):
    if x == '.': return 0
    elif x == '#': return 1

def deeptup(ls):
    return tuple(tuple(x) for x in ls)

shapes = [np.array([list(map(f, s)) for s in lines[5*i+1:5*i+4]]) for i in range(6)]
regions = lines[30:]

ans = 0
for i,region in enumerate(regions):
    size, pres = region.split(':')
    size = [int(x) for x in size.split('x')]
    pres = [int(x) for x in pres.split()]
    pres2 = []
    for i in range(len(pres)):
        if i > 0:
            pres2 += [i] * pres[i]

    A = np.zeros(shape=tuple(size[::-1]))
    Q = deque([(np.copy(A), 0)])
    seen = set([(deeptup(A), 0)])
    while Q:
        B, k = Q.popleft()
        print(B, k)
        if k == len(pres2):
            ans += 1
            break
        for dr in range(B.shape[0] - 3 + 1):
            for dc in range(B.shape[1] - 3 + 1):
                shap = np.copy(shapes[pres2[k]])
                for j in range(8):
                    B[dr:dr+3,dc:dc+3] += shap
                    Btup = deeptup(B)
                    #print(B, np.any(B > 1), Btup)
                    if np.any(B > 1):
                        B[dr:dr+3,dc:dc+3] -= shap
                        continue
                    if (Btup, k+1) in seen:
                        B[dr:dr+3,dc:dc+3] -= shap
                        continue
                    Q.append((np.copy(B), k+1))
                    seen.add((Btup, k+1))
                    B[dr:dr+3,dc:dc+3] -= shap

                    if j == 3:
                        shap = np.flip(shap)
                    else:
                        shap = np.rot90(shap)
print(ans)