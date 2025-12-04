with open("inputs/day04.txt") as f:
    data = f.read()

lines = data.strip().split("\n")
grid = [[c for c in line] for line in lines]


rolls = set()

for y, line in enumerate(grid):
    for x, cell in enumerate(line):
        if cell == "@":
            rolls.add((x, y))


def count8Neighbors(coord, rolls):
    x, y = coord
    neighCount = 0

    if (x - 1, y - 1) in rolls:
        neighCount += 1
    if (x, y - 1) in rolls:
        neighCount += 1
    if (x + 1, y - 1) in rolls:
        neighCount += 1
    if (x + 1, y) in rolls:
        neighCount += 1
    if (x + 1, y + 1) in rolls:
        neighCount += 1
    if (x, y + 1) in rolls:
        neighCount += 1
    if (x - 1, y + 1) in rolls:
        neighCount += 1
    if (x - 1, y) in rolls:
        neighCount += 1

    return neighCount


reachableCount = 0

for x, y in rolls:
    if count8Neighbors((x, y), rolls) < 4:
        reachableCount += 1

print("Part 1", reachableCount)

# Part 2 : remove rolls from rolls if they are reachable
# Until it stabilizes

initialSize = len(rolls)
isStabilized = False

while not isStabilized:
    print(f"we have {len(rolls)}, remove!")
    sizeBeforeRemoval = len(rolls)
    rolls = [(x, y) for (x, y) in rolls if count8Neighbors((x, y), rolls) >= 4]
    isStabilized = len(rolls) == sizeBeforeRemoval

print("Part 2", initialSize - len(rolls))
