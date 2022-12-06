#!/usr/bin/env python3

import sys
from collections import defaultdict


def find_first_distinct_set(letters, n):
    counts = defaultdict(lambda: 0)
    for idx, char in enumerate(letters):
        counts[char] += 1
        if idx - n >= 0:
            counts[letters[idx-n]] -= 1
        if sum(counts.values()) == n and all(c <= 1 for c in counts.values()):
            return idx + 1

def part1(lines):
    for line in lines:
        line = line.strip()
        if not line:
            break
        return find_first_distinct_set(line, 4)


def part2(lines):
    for line in lines:
        line = line.strip()
        if not line:
            break
        return find_first_distinct_set(line, 14)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

