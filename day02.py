with open("inputs/day02.txt", "r") as file:
    data = file.read()

ranges = [
    (int(range.split("-")[0]), int(range.split("-")[1]))
    for range in data.strip().split(",")
]

print("Total ids to consider", sum([r[1] - r[0] for r in ranges]))


def isInvalidPart1(id):
    idStr = str(id)
    size = len(idStr)
    if len(idStr) % 2 != 0:
        return False

    return idStr[size // 2 :] == idStr[: size // 2]


def isInvalidPart2(id):
    idStr = str(id)
    size = len(idStr)

    # Find integer factors
    factors = []
    for f in range(1, size // 2 + 1):
        if size % f == 0:
            factors.append(f)

    for f in factors:
        # Split idStr into groups of f length
        nbGroups = size // f
        groups = []
        for gIdx in range(nbGroups):
            groups.append(idStr[gIdx * f : gIdx * f + f])

        # Check if all groups are identical
        if len(set(groups)) == 1:
            return True

    return False


invalidAccumulatorPart1 = 0
invalidAccumulatorPart2 = 0


for r in ranges:
    for id in range(r[0], r[1] + 1):
        if isInvalidPart1(id):
            assert isInvalidPart2(id)  # test case for part 2 ;)
            invalidAccumulatorPart1 += id


for r in ranges:
    for id in range(r[0], r[1] + 1):
        if isInvalidPart2(id):
            invalidAccumulatorPart2 += id

print("Part 1:", invalidAccumulatorPart1)
print("Part 2:", invalidAccumulatorPart2)
