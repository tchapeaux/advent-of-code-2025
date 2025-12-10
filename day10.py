from itertools import combinations
from typing import List, Set, Tuple

from pulp import PULP_CBC_CMD, LpMinimize, LpProblem, LpVariable, value

with open("inputs/day10.txt") as f:
    data = f.read().strip().split("\n")

LightsState = Tuple[bool, ...]
Button = Tuple[int, ...]
JoltageReq = Tuple[int, ...]

MachineConfig = Tuple[LightsState, Tuple[Button, ...], JoltageReq]

machines: Set[MachineConfig] = set()

for line in data:
    words = line.split(" ")

    lightsRaw = words[0][1:-1]
    lights: LightsState = tuple([True if char == "#" else False for char in lightsRaw])

    joltageRaw = words[-1][1:-1].split(",")
    joltages: JoltageReq = tuple([int(x) for x in joltageRaw])

    buttonsConfigRaw = words[1:-1]
    buttonsConfig: List[Button] = []
    for bC in buttonsConfigRaw:
        lightsToggled = tuple([int(x) for x in bC[1:-1].split(",")])
        buttonsConfig.append(lightsToggled)

    assert len(lights) == len(joltages)

    machines.add((lights, tuple(buttonsConfig), joltages))

# Let's think about Part 1
# For each machine, any button needs to be pressed at most once
# So it's just about finding the correct combinations of buttons to press once


def findFewestPresses(machine: MachineConfig) -> int:
    (lights, buttonsConfig, joltage) = machine

    # Brute-force all combinations of buttons to find the correct one
    for combSize in range(1, len(buttonsConfig)):
        for buttons in combinations(buttonsConfig, combSize):
            buttonsFinalState = tuple(
                [
                    sum([b.count(lightIdx) for b in buttons]) % 2 == 1
                    for lightIdx in range(len(lights))
                ]
            )

            if buttonsFinalState == lights:
                return combSize

    # Could not find a combination
    raise Exception("Could not find button combination")


accPart1 = 0

for mIdx, m in enumerate(machines):
    presses = findFewestPresses(m)
    accPart1 += presses

print("Part 1:", accPart1)

# Now for part 2, we need to track separate counters


def solvePart2LinearProg(targets, buttons):
    # We will solve this with linear programming
    # https://www.coin-or.org/PuLP/pulp.html

    # First we need to convert the problem into the correct format

    prob = LpProblem("Find_fewest_button_presses", LpMinimize)

    variables = [
        LpVariable(str(vIdx), lowBound=0, cat="Integer") for vIdx in range(len(buttons))
    ]

    # Define objective
    prob += sum(variables), "Objective"
    # Define one constraint per counter
    for tIdx, tValue in enumerate(targets):
        relatedVariables = [
            v for vIdx, v in enumerate(variables) if tIdx in buttons[vIdx]
        ]

        prob += sum(relatedVariables) == tValue, f"Counter_{tIdx}"

    # Then we can solve using pulp!

    prob.solve(PULP_CBC_CMD(msg=False))

    if prob.status != 1:
        raise Exception("Could not solve equation")

    return int(value(prob.objective))


accPart2 = 0

for mIdx, (lights, buttons, joltages) in enumerate(machines):
    presses = solvePart2LinearProg(joltages, buttons)
    accPart2 += presses

print("Part 2:", accPart2)
