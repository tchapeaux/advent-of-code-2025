with open("inputs/day01.txt", "r") as file:
    data = file.read()

lines = data.strip().split("\n")

instructions = [(line[0], int(line[1:])) for line in lines]


currentValue = 50

part1Counter = 0
part2Counter = 0

for instruction in instructions:
    direction, distance = instruction

    dirValue = 1 if direction == "R" else -1

    for i in range(distance):
        currentValue += dirValue
        currentValue %= 100

        if currentValue == 0:
            part2Counter += 1

    if currentValue == 0:
        part1Counter += 1


print(currentValue)
print(part1Counter)
print(part2Counter)
