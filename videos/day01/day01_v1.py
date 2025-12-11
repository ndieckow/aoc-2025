rots = open("in.txt").read().splitlines()

def rotate(dial, d, amt):
    if d == 'L':
        amt *= -1
    return (dial + amt) % 100

dial = 50
ans = 0
for rot in rots:
    d, amt = rot[0], int(rot[1:])
    dial = rotate(dial, d, amt)
    if dial == 0:
        ans += 1

print("Part 1:", ans)