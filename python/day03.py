#!/usr/bin/env python3

import sys
import math
import string
from collections import defaultdict


def priority(letter):
    return string.ascii_letters.find(letter) + 1


def part1(lines):
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            break
        size = len(line) / 2
        counts = defaultdict(lambda: 0)
        for (idx, letter) in enumerate(line):
            side = math.floor(idx / size) + 1
            counts[letter] |= side

        found = [c for c in counts if counts[c] == 3][0]
        total += priority(found)

    return total


def grouped(lines, count):
    group = []
    for line in lines:
        group.append(line)
        if len(group) == count:
            yield group
            group = []
    if len(group):
        yield group


def part2(lines):
    total = 0
    for group in grouped(map(str.strip, lines), 3):
        if len(group) < 3:
            continue
        counts = defaultdict(lambda: 0)
        for (idx, line) in enumerate(group):
            for letter in line:
                counts[letter] |= 2**idx
        found = [c for c in counts if counts[c] == 7][0]
        total += priority(found)

    return total


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

