inp = open("05.in").read()

ranges, nums = inp.split('\n\n')
ranges = [
    tuple(int(x) for x in ran.split('-'))
    for ran in ranges.split('\n')
]
nums = [int(x) for x in nums.split('\n')]

ans = 0
for n in nums:
    for l, u in ranges:
        if l <= n <= u:
            ans += 1
            break
print("Part 1:", ans)

ans2 = 0
max_u = -1
for l, u in sorted(ranges):
    if l > max_u:
        ans2 += u - l + 1
    elif u > max_u:
        ans2 += u - max_u
    max_u = max(max_u, u)
print("Part 2:", ans2)