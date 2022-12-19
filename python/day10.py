#!/usr/bin/env python3

import sys
from math import floor


def parse_instructions(lines):
    instructions = []
    for line in lines:
        line = line.strip()
        if not line:
            break
        opcode, *values = line.split()
        instructions.append((opcode, [int(x) for x in values]))
    return instructions


class CPU:
    def __init__(self, instructions):
        self._instructions = instructions
        self.reset()

    def reset(self):
        self._x = 1
        self._cycle = 0

    def tick(self):
        self._cycle += 1
        return (self._x, self._cycle)

    def step(self):
        for (opcode, values) in self._instructions:
            if opcode == 'noop':
                yield self.tick()
            elif opcode == 'addx':
                yield self.tick()
                yield self.tick()
                self._x += values[0]

    def run(self):
        for _ in self.step():
            pass

    def x(self):
        return self._x


def part1(lines):
    cpu = CPU(parse_instructions(lines))
    strength = []
    for x, cycle in cpu.step():
        if cycle == 20 or (cycle - 20) % 40 == 0:
            strength.append(cycle * x)
    return sum(strength)


def part2(lines):
    width = 40
    height = 6
    crt = [['.'] * width for _ in range(height)]
    cpu = CPU(parse_instructions(lines))

    for x, cycle in cpu.step():
        cy = floor((cycle - 1) / width)
        cx = (cycle - 1) % width
        if x >= cx-1 and x <= cx+1:
            crt[cy][cx] = '#'

    for y in range(height):
        print(''.join(crt[y]))


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

