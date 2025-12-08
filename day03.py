banks = open("03.in").read().splitlines()

def argmax(nums):
    maxv, maxi = 0, None
    for i,n in enumerate(nums):
        if n > maxv:
            maxv = n
            maxi = i
    return maxv, maxi

def solve(bank, k):  # k=2 for part 1, k=12 for part 2
    nums = [int(x) for x in bank]
    ansnums = []
    N = len(nums)
    offset = 0
    for i in range(k):
        maxv, maxi = argmax(nums[offset : N-(k-1)+i])
        offset += maxi+1
        ansnums.append(maxv)
    return sum([10**i * v for i,v in enumerate(ansnums[::-1])])

for part, k in [(1, 2), (2, 12)]:
    ans = 0
    for bank in banks:
        ans += solve(bank, k)
    print(f"Part {part}: {ans}")