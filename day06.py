import numpy as np

lines = open("06.in").read().splitlines()
nums, ops = [[int(x) for x in s.split()] for s in lines[:-1]], lines[-1].split()
nums_arr = np.array(nums)

ans = 0
for i,op in enumerate(ops):
    if op == '+':
        ans += np.sum(nums_arr[:,i])
    else:
        ans += np.prod(nums_arr[:,i])
print("Part 1:", ans)

# PART 2
arr = np.array([list(x) for x in lines]).T
ans2 = 0
buf = 0
op = None

for i,row in enumerate(arr):
    if row[-1] != ' ':
        op = row[-1]
        ans2 += buf
        buf = 0 if op == '+' else 1
    s = ''.join(row[:-1]).strip()
    if s == '':
        continue
    num = int(s)
    if op == '+':
        buf += num
    else:
        buf *= num
ans2 += buf
print("Part 2:", ans2)