#!/usr/bin/env python3

import sys


def parse_pairs(lines):
    pairs = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        pair = [[int(n) for n in rng.split("-")] for rng in line.split(",")]
        pairs.append(pair)
    return pairs


def pairs_contain(p1, p2):
    s1 = set(range(p1[0], p1[1] + 1))
    s2 = set(range(p2[0], p2[1] + 1))
    return s1.issuperset(s2) or s2.issuperset(s1)


def pairs_overlap(p1, p2):
    s1 = set(range(p1[0], p1[1] + 1))
    s2 = set(range(p2[0], p2[1] + 1))
    return not s1.isdisjoint(s2)


def part1(lines):
    count = 0
    pairs = parse_pairs(lines)
    for [p1, p2] in pairs:
        if pairs_contain(p1, p2):
            count += 1
    return count


def part2(lines):
    count = 0
    pairs = parse_pairs(lines)
    for [p1, p2] in pairs:
        if pairs_overlap(p1, p2):
            count += 1
    return count


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

