from collections import deque
from functools import lru_cache

with open("inputs/day07.txt") as f:
    data = f.read().strip()

lines = data.split("\n")

startPos = None
splitters = set()

for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == "S":
            startPos = (x, y)
        if lines[y][x] == "^":
            splitters.add((x, y))

assert startPos
assert len(splitters) > 0

maxY = max([pos[1] for pos in splitters])

# Handle all emitters in FIFO, generating more emitters as we go
# Check which emitters have already been generated to avoid double-counting

splitCount = 0
emitters = deque([startPos])
alreadyHandled = set([startPos])

while len(emitters) > 0:
    pos = emitters.popleft()

    x = pos[0]
    # Find the closest splitter directly below it
    try:
        closestY = min([s[1] for s in splitters if s[0] == x and s[1] > pos[1]])
    except ValueError:
        # No splitter encountered, skip
        continue

    if (x, closestY) in alreadyHandled:
        continue

    # Split detected
    splitCount += 1

    # Generate 2 new emitters
    emitters.append((x - 1, closestY))
    emitters.append((x + 1, closestY))

    alreadyHandled.add((x, closestY))

print("Part 1", splitCount)

# Part 2 : count multi-worlds


@lru_cache
def countTimelines(startPoint, splittersBelow):
    if len(splittersBelow) == 0:
        return 1

    try:
        closestSplitterY = min(
            [
                s[1]
                for s in splittersBelow
                if s[0] == startPoint[0] and s[1] > startPoint[1]
            ]
        )
    except ValueError:
        return 1

    countLeft = countTimelines(
        (startPoint[0] - 1, closestSplitterY),
        tuple([s for s in splittersBelow if s[1] > closestSplitterY]),
    )

    countRight = countTimelines(
        (startPoint[0] + 1, closestSplitterY),
        tuple([s for s in splittersBelow if s[1] > closestSplitterY]),
    )

    return countLeft + countRight


print("Part 2", countTimelines(startPos, tuple(splitters)))
