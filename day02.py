from math import ceil

ranges = open("02.in").read().split(',')

def splitint(x):
    if len(x) == 1:
        return x, None
    return int(x[:len(x)//2]), int(x[len(x)//2:])

def duplicate(n):
    d = 1
    v = n
    while v > 0:
        v //= 10
        d *= 10
    return n*d + n

ans = 0
for ran in ranges:
    l, u = ran.split('-')
    if len(l) == len(u) and len(l) % 2 == 1:
        continue
    la, lb = splitint(l)
    ua, ub = splitint(u)

    hl = len(u) // 2
    if len(l) % 2 == 1:
        la, lb = 10**(hl-1), 0
    elif len(u) % 2 == 1:
        ua = 10**hl - 1
        ub = ua

    for i in range(la, ua+1):
        if i == la and i < lb:
            continue
        if i == ua and i > ub:
            continue
        ans += duplicate(i)

print("Part 1:", ans)

# PART 2
ans2 = 0
for ran in ranges:
    l, u = ran.split('-')
    ll, ul = len(l), len(u)
    lint, uint = int(l), int(u)
    
    # ensure that all values have the same length
    if ll < ul:
        tmp = 10**(ul - 1)
        ranges.append(str(tmp) + '-' + u)
        u = str(tmp - 1)
    
    # only use ll from this point
    ldiv = [i for i in range(1, ll // 2 + 1) if ll % i == 0]
    nums = set()
    for d in ldiv:
        r = ll // d
        for i in range(10**(d-1), 10**d):
            n = int(str(i) * r)
            if lint <= n <= uint:
                nums.add(n)
    ans2 += sum(nums)
print("Part 2:", ans2)