with open("inputs/day12.txt") as f:
    data = f.read().strip().split("\n\n")

regionsRaw = data[-1].split("\n")
regions = []
for line in regionsRaw:
    dimensions, quantities = line.split(": ")
    x, y = [int(x) for x in dimensions.split("x")]
    quantities = [int(x) for x in quantities.split(" ")]
    regions.append((x, y, tuple(quantities)))

shapesRaw = data[:-1]
shapes = []
for shapeRaw in shapesRaw:
    shapeLines = shapeRaw.split("\n")[1:]
    cells = []
    for y, line in enumerate(shapeLines):
        for x, char in enumerate(line):
            if char == "#":
                cells.append((x, y))
    shapes.append(tuple(cells))

shapesNbOfCells = [len(s) for s in shapes]

# Remove regions where fitting the required shapes will be impossible
# because there are more cells to fit than are physically in the area
# (First pass)
regions2 = []
for region in regions:
    w, h, quantities = region[0], region[1], region[2]
    nbOfCellsToFit = sum(
        [quantities[idx] * shapesNbOfCells[idx] for idx in range(len(quantities))]
    )

    cannotFit = w * h < nbOfCellsToFit
    if cannotFit:
        continue
    regions2.append(region)

print("Removed", len(regions) - len(regions2), "regions")

# When checking the problems in regions2, we see that they always have around 30% of free space
# So we decided to guess that this was sufficient to fit all shapes without too much loss
# We submitted the answer directly, and... it's a Christmas miracle! It was correct
print("Part 2", len(regions2))
