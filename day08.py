from itertools import combinations
from typing import List, Set, Tuple

with open("inputs/day08.txt") as f:
    data = f.read().strip()

LINK_LIMIT = 1000


Box = Tuple[int, int, int]
Edge = Tuple[Box, Box]
Circuit = Set[Box]

boxes: List[Box] = [
    tuple(int(x) for x in line.split(","))
    for line in data.split("\n")  # type: ignore
]

assert all([len(b) == 3 for b in boxes])

edges: List[Edge] = []

circuits: List[Circuit] = [set([b]) for b in boxes]


# We will use the distance squared for distance comparison,
# so that we avoid a costly sqrt
# and because if a distance is higher, its square is also higher


def distanceSquared(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return dx * dx + dy * dy + dz * dz


# Go through each box pair and maintain the top 10 shortest distance

print("Building all pairs dist...")
allPairsDist: List[Tuple[int, Box, Box]] = []
for p1, p2 in combinations(boxes, 2):
    allPairsDist.append((distanceSquared(p1, p2), p1, p2))


# Main loop of creating circuits by taking the closest boxes one by one
print("Sorting all dist...")
sortedPairsDist = sorted(allPairsDist)
for dist, box1, box2 in sortedPairsDist:
    shortestLink = (box1, box2)

    # Add link and add to circuits
    (box1, box2) = shortestLink

    box1Circuit = set([box1])
    box2Circuit = set([box2])
    for circuit in circuits:
        if box1 in circuit:
            box1Circuit = circuit
        if box2 in circuit:
            box2Circuit = circuit

    newCircuit = set()
    newCircuit |= box1Circuit
    newCircuit |= box2Circuit

    circuits = [c for c in circuits if c != box1Circuit and c != box2Circuit] + [
        newCircuit
    ]

    edges.append(shortestLink)

    # Part 1 end condition
    if len(edges) == LINK_LIMIT:
        circuitsByLength = sorted(circuits, key=lambda x: len(x), reverse=True)
        print(
            "Part 1",
            len(circuitsByLength[0])
            * len(circuitsByLength[1])
            * len(circuitsByLength[2]),
        )

    # Part 2 end condition
    if len(circuits) == 1:
        print("Part 2", box1[0] * box2[0])
        break

print("Finished")
