banks = open("03.in").read().splitlines()

def argmax(nums):
    maxv, maxi = 0, None
    for i,n in enumerate(nums):
        if n > maxv:
            maxv, maxi = n, i
    return maxv, maxi

def solve(bank, k):
    nums = [int(x) for x in bank]
    N = len(nums)
    offset = 0
    ans = 0
    for j in range(k):
        subnums = nums[offset : N-(k-1)+j]
        d, max_i = argmax(subnums)
        offset += max_i + 1
        ans += d * 10**(k-j-1)
    return ans

ans = 0
ans2 = 0
for bank in banks:
    ans += solve(bank, 2)
    ans2 += solve(bank, 12)
print("Part 1:", ans)
print("Part 2:", ans2)