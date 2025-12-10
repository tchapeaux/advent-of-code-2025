import math
from functools import cache

with open("inputs/day03.txt", "r") as file:
    data = file.read()

lines = data.strip().split("\n")

cells = [[int(c) for c in line] for line in lines]


def findBestPair(cells):
    bestDecimal = -1
    bestUnit = -1

    for cIdx, c in enumerate(cells):
        if cIdx < len(cells) - 1 and (bestDecimal == -1 or c > bestDecimal):
            bestDecimal = c
            bestUnit = -1
        elif bestDecimal > 0 and (bestUnit == -1 or c > bestUnit):
            bestUnit = c

    assert bestDecimal != -1 and bestUnit != -1
    return 10 * bestDecimal + bestUnit


# print(findBestPair([1, 1, 8, 3, 9, 2]))

part1Acc = 0
for line in cells:
    part1Acc += findBestPair(line)

print("Part 1", part1Acc)


@cache
def findBestCombination(cells, combSize):
    assert combSize > 0

    if len(cells) < combSize:
        return -1

    if len(cells) == combSize:
        return int("".join([str(c) for c in cells]))

    if combSize == 1:
        return max(cells)

    # Recursively find the best with and without taking the first cell
    # Then keep the best best one

    firstTaken = cells[0] * int(math.pow(10, combSize - 1))

    bestWith = firstTaken + findBestCombination(cells[1:], combSize - 1)
    bestWithout = findBestCombination(cells[1:], combSize)

    return max(bestWith, bestWithout)


## Debug
# print(findBestCombination((1, 1, 8, 3, 9, 2), 2))
# print(findBestCombination(tuple(int(x) for x in "987654321111111"), 12))
# print(findBestCombination(tuple(int(x) for x in "811111111111119"), 12))
# print(findBestCombination(tuple(int(x) for x in "234234234234278"), 12))
# print(findBestCombination(tuple(int(x) for x in "818181911112111"), 12))

part2Acc = 0
for line in cells:
    part2Acc += findBestCombination(tuple(line), 12)

print("Part 2", part2Acc)
