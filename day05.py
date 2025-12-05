from typing import List, Tuple

Range = Tuple[int, int]

with open("inputs/day05.txt") as f:
    data = f.read().strip()

ranges: List[Range] = []
itemsIds = set()

(rangesRaw, itemsIdsRaw) = data.split("\n\n")

for range in rangesRaw.split("\n"):
    parts = [int(x) for x in range.split("-")]
    ranges.append((parts[0], parts[1]))

for itemId in itemsIdsRaw.split("\n"):
    itemsIds.add(int(itemId))


def isInRange(itemId, range):
    return range[0] <= itemId <= range[1]


part1Count = 0

for itemId in itemsIds:
    if any([isInRange(itemId, range) for range in ranges]):
        part1Count += 1

print("Part 1", part1Count)


#### PART TWO - Let's merge ranges


def mergeTwoRanges(rangeA: Range, rangeB: Range) -> List[Range]:
    # Because we are in integer space,
    # we consider "adjacent ranges" such as [0, 1], [2, 3] to be overlapping
    # in the sense that they must be merged

    # If separated, then return both ranges
    if max(rangeA) + 1 < min(rangeB) or max(rangeB) + 1 < min(rangeA):
        return [rangeA, rangeB]

    # Otherwise, we know there is at least some overlap, so we can return the aggregate
    return [(min(rangeA[0], rangeB[0]), max(rangeA[1], rangeB[1]))]


def addRangeToAggregate(aggregatedRanges: List[Range], newRange: Range) -> List[Range]:
    # Try to merge with all ranges in the aggregate
    # If we detect a merge, don't add it to the aggregate yet, but restart the process with this new merged range

    for range in aggregatedRanges:
        result = mergeTwoRanges(range, newRange)
        if len(result) == 1:
            # merge detected
            mergedRange = result[0]
            # Remove merged range
            newAggregate = [r for r in aggregatedRanges if r is not range]
            return addRangeToAggregate(newAggregate, mergedRange)

    # if we reach here, then no merge has been detected
    # Simply return the aggregate with the new range
    return sorted(aggregatedRanges + [newRange])


def rangeSize(range: Range):
    return max(range) - min(range) + 1


# Let's create an aggregate one by one

aggregateRanges = []

for range in ranges:
    aggregateRanges = addRangeToAggregate(aggregateRanges, range)

print("Part 2", sum(rangeSize(r) for r in aggregateRanges))
