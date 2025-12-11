rots = open("in.txt").read().splitlines()

def rotate(dial, d, amt):
    quo, rem = divmod(amt, 100)
    zeros = quo
    if d == 'L':
        rem *= -1
        amt *= -1
    if dial and not (0 <= dial + rem <= 100):
        zeros += 1
    return (dial + amt) % 100, zeros

dial = 50
ans = 0
ans2 = 0
for rot in rots:
    d, amt = rot[0], int(rot[1:])
    dial, zeros = rotate(dial, d, amt)
    ans2 += zeros
    if dial == 0:
        ans += 1

print("Part 1:", ans)
print("Part 2:", ans + ans2)