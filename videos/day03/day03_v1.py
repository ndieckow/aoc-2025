banks = open("03.in").read().splitlines()

def argmax(nums):
    maxv, maxi = 0, None
    for i,n in enumerate(nums):
        if n > maxv:
            maxv = n
            maxi = i
    return maxv, maxi

def solve(bank):
    nums = [int(x) for x in bank]
    d1, i = argmax(nums[:-1])
    d2 = max(nums[i+1:])
    return 10 * d1 + d2

ans = 0
for bank in banks:
    ans += solve(bank)
print("Part 1:", ans)