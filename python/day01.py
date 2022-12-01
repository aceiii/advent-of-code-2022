#!/usr/bin/env python3

import sys


def part1(lines):
    totals = [0]
    for line in lines:
        try:
            totals[-1] += int(line)
        except:
            totals.append(0)

    return max(totals)


def part2(lines):
    totals = [0]
    for line in lines:
        try:
            totals[-1] += int(line)
        except:
            totals.append(0)

    return sum(sorted(totals, reverse=True)[:3])


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

