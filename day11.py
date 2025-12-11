from copy import deepcopy
from typing import Dict, Set, Tuple

with open("inputs/day11.txt") as f:
    data = f.read().strip().split("\n")

Edges = Dict[str, Tuple[str, ...]]

edges: Edges = dict()

for line in data:
    source, dests = line.strip().split(":")
    edges[source] = tuple(dests.strip().split(" "))

start_cell = "you"
end_cell = "out"

assert start_cell in edges
assert any([end_cell in dests for dests in edges.values()])

# Find all path by exploring depth-first
Path = Tuple[str, ...]
paths: Set[Path] = set()


def yieldPaths(
    currentPath: Path, edges: Edges, end_cell: str, forbiddenCells: Tuple[str, ...]
):
    assert len(currentPath) > 0
    currentCell = currentPath[-1]

    # print(currentPath[0], end_cell, "-".join(currentPath))

    if currentCell not in edges:
        return

    dests = edges[currentCell]

    for dest in dests:
        if dest in currentPath or dest in forbiddenCells:
            # no loops
            continue

        if dest == end_cell:
            yield currentPath + (dest,)

        else:
            newPath = currentPath + (dest,)
            for subpath in yieldPaths(newPath, edges, end_cell, forbiddenCells):
                yield subpath


def pruneIrrelevant(fromCell: str, toCell: str, edges: Edges) -> Edges:
    # Return a pruned version of edges where irrelevant nodes are removed
    # (for paths from fromCell to toCell)

    newEdges = deepcopy(edges)

    # Create a full list of nodes, including destination leaves
    nodes = set(newEdges.keys())
    for dests in newEdges.values():
        for d in dests:
            nodes.add(d)

    hasChanged = True
    while hasChanged:
        hasChanged = False

        nodesToRemove = set()
        for node in nodes:
            if node == fromCell or node == toCell:
                continue

            # Remove node with no destination
            if node not in newEdges or len(newEdges[node]) == 0:
                nodesToRemove.add(node)

            # Remove node which are not pointed to
            if not any([node in dests for dests in newEdges.values()]):
                nodesToRemove.add(node)

        if len(nodesToRemove) > 0:
            nodes = nodes.difference(nodesToRemove)
            hasChanged = True

        newNewEdges = dict()
        for start, dests in edges.items():
            if start in nodes and not all([d not in nodes for d in dests]):
                newNewEdges[start] = [d for d in dests if d in nodes]
        newEdges = newNewEdges

    with open(f"artifacts/day11_{fromCell}_{toCell}", "w") as f:
        for start, dests in newEdges.items():
            f.write(f"{start}: {' '.join(dests)}\n")

    return newEdges


def countPathsBetween(fromCell, toCell, forbiddenCells=()):
    prunedEdges = pruneIrrelevant(fromCell, toCell, edges)

    return len(list(yieldPaths((fromCell,), prunedEdges, toCell, forbiddenCells)))


print("Part 1", countPathsBetween(start_cell, end_cell))


# Part 2


svr_cell = "svr"
dac_cell = "dac"
fft_cell = "fft"
assert svr_cell in edges
assert dac_cell in edges
assert fft_cell in edges

# Looking at the data, we noticed that there is no way to go from DAC to FFT
DACtoFFT = countPathsBetween(dac_cell, fft_cell, (svr_cell, end_cell))
assert DACtoFFT == 0
# This means that we should only consider SVR-FFT-DAC-OUT paths
# (This is only the case for our input, this will break the examples)


SVRtoFFT = countPathsBetween(svr_cell, fft_cell, (dac_cell, end_cell))
print("SVRtoFFT", SVRtoFFT)
FFTtoDAC = countPathsBetween(fft_cell, dac_cell, (svr_cell, end_cell))
print("FFTtoDAC", FFTtoDAC)
DACtoEND = countPathsBetween(dac_cell, end_cell, (fft_cell, svr_cell))
print("DACtoEND", DACtoEND)

print("Part 2", SVRtoFFT * FFTtoDAC * DACtoEND)
