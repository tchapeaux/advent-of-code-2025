import re

with open("inputs/day06.txt") as f:
    data = f.read().strip()

lines = [re.sub(" +", " ", line).strip().split(" ") for line in data.split("\n")]

nbOfProblems = len(lines[0])
assert all([len(line) == nbOfProblems for line in lines])

accPart1 = 0

for colIdx in range(nbOfProblems):
    operator = lines[-1][colIdx]
    accProblem = 0 if operator == "+" else 1
    for row in lines[:-1]:
        if operator == "+":
            accProblem += int(row[colIdx])
        else:
            accProblem *= int(row[colIdx])

    accPart1 += accProblem

print("Part 1", accPart1)

# Part 2 : parse the weird vertical alignment

lines2 = data.split("\n")
maxLenLine = max([len(line) for line in lines2])

# pad all lines so they have the same length
lines2 = [line.ljust(maxLenLine, " ") for line in lines2]

# Find col idx separators of problems

pbSeparators = [-1]  # -1 is for the first problem

for colIdx in range(maxLenLine):
    if all([colIdx >= len(line) or line[colIdx] == " " for line in lines2]):
        pbSeparators.append(colIdx)

# Parse problem parameters for each problem

problems = []

for sepIdx in range(len(pbSeparators)):
    pbStartCol = pbSeparators[sepIdx] + 1
    pbEndCol = (
        pbSeparators[sepIdx + 1] if sepIdx < len(pbSeparators) - 1 else maxLenLine
    )
    problemLines = [line[pbStartCol:pbEndCol] for line in lines2]
    problems.append(problemLines)

accPart2 = 0

for prob in problems:
    operator = prob[-1].strip()

    acc = 0 if operator == "+" else 1

    for colIdx in range(len(prob[0])):
        operand = int("".join([p[colIdx] for p in prob[:-1]]).strip())
        if operator == "+":
            acc += operand
        else:
            acc *= operand
    accPart2 += acc


print("Part 2", accPart2)
