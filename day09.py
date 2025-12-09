from itertools import combinations

with open("inputs/day09_example.txt") as f:
    data = f.read().strip()

tiles = [tuple(int(x) for x in line.split(",")) for line in data.split("\n")]


def areaOf(t1, t2):
    return (abs(t2[1] - t1[1]) + 1) * (abs(t2[0] - t1[0]) + 1)


sortedAreas = list(
    reversed(sorted([(areaOf(t1, t2), t1, t2) for t1, t2 in combinations(tiles, 2)]))
)

print("Part 1", sortedAreas[0][0], sortedAreas[0][1], sortedAreas[0][2])

# Part 2 left as an exercise to the reader
