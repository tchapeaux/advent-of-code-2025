import { readFileSync } from "fs";

const input = readFileSync(`inputs/day01.txt`, "utf8");

const data = input
  .trim()
  .split("\n")
  .map((line) => [line.trim()[0], parseInt(line.trim().slice(1))]);

function part1() {
  let currentValue = 50;
  let zeroCount = 0;

  for (const [direction, distance] of data) {
    if (direction === "L") {
      currentValue -= distance;
    } else if (direction === "R") {
      currentValue += distance;
    } else {
      throw new Error(`Invalid direction: ${direction}`);
    }

    currentValue %= 100;

    if (currentValue < 0) {
      currentValue += 100;
    }

    if (currentValue === 0) {
      zeroCount++;
    }
  }

  console.log(currentValue);
  console.log(zeroCount);
}

part1();

function part2() {
  let currentValue = 50;
  let zeroCount = 0;

  for (const [direction, distance] of data) {
    const delta = direction === "L" ? -1 : 1;

    for (let step = 0; step < distance; step++) {
      currentValue += delta;
      currentValue %= 100;

      if (currentValue < 0) {
        currentValue += 100;
      }

      if (currentValue === 0) {
        zeroCount++;
      }
    }
  }
  console.log(currentValue);
  console.log(zeroCount);
}

part2();
