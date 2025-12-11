from collections import defaultdict
from functools import cache

inp = open("11.in").read().splitlines()

adj = defaultdict(list)

for line in inp:
    a, b = line.split(':')
    adj[a] = b.split()

@cache
def dp(s, t):
    if s == t:
        return 1
    return sum(dp(w, t) for w in adj[s])

print("Part 1:", dp('you', 'out'))

ans2 = dp('svr', 'fft') * dp('fft', 'dac') * dp('dac', 'out')
ans2 += dp('svr', 'dac') * dp('dac', 'fft') * dp('fft', 'out')
print("Part 2:", ans2)