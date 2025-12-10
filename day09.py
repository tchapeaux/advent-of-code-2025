from itertools import combinations
from math import copysign

with open("inputs/day09.txt") as f:
    data = f.read().strip()

tiles = [tuple(int(x) for x in line.split(",")) for line in data.split("\n")]


def areaOf(t1, t2):
    return (abs(t2[1] - t1[1]) + 1) * (abs(t2[0] - t1[0]) + 1)


sortedAreas = list(
    reversed(sorted([(areaOf(t1, t2), t1, t2) for t1, t2 in combinations(tiles, 2)]))
)

print("Part 1", sortedAreas[0][0], sortedAreas[0][1], sortedAreas[0][2])

# Part 2

segments = []
for tIdx in range(len(tiles) - 1):
    segments.append((tiles[tIdx], tiles[tIdx + 1]))
segments.append((tiles[len(tiles) - 1], tiles[0]))


def isInsideArea(t1, t2, point):
    minx = min(t1[0], t2[0])
    maxx = max(t1[0], t2[0])
    miny = min(t1[1], t2[1])
    maxy = max(t1[1], t2[1])

    return minx < point[0] < maxx and miny < point[1] < maxy


def yieldPointInSegment(t1, t2):
    dx = 0 if t1[0] == t2[0] else int(copysign(1, t2[0] - t1[0]))
    dy = 0 if t1[1] == t2[1] else int(copysign(1, t2[1] - t1[1]))

    yield t1
    current = t1
    while current != t2:
        current = (current[0] + dx, current[1] + dy)
        yield current


# Check areas from largest to smallest and return the first one
# where no segments intersects

# NOTE - this actually could find an "outer rectangle", which fits nicely into the
# tiles shape, but thankfully this does not happen in my input ...

for areaIdx, (area, t1, t2) in enumerate(sortedAreas):
    if areaIdx % 100 == 0:
        print("check", area, areaIdx, len(sortedAreas))

    # Check if a segment intersects
    hasFoundInnerPoint = False
    for s in segments:
        if hasFoundInnerPoint:
            break

        for p in yieldPointInSegment(s[0], s[1]):
            # print("is", p, "in", t1, t2)
            if isInsideArea(t1, t2, p):
                # print("found inner point")
                hasFoundInnerPoint = True
                break

    else:
        if not hasFoundInnerPoint:
            # If we reach here, no inner point was found
            print("Part 2", area, t1, t2)
            exit(0)
