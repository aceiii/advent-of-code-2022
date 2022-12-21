#!/usr/bin/env python3

import sys
import json
from functools import cmp_to_key


def parse_pairs(lines):
    pairs = []
    left = None
    right = None
    for line in lines:
        line = line.strip()
        if left is not None and right is not None:
            pairs.append((left, right))
            left = None
            right = None
            continue
        packet = json.loads(line)
        if left is None:
            left = packet
        else:
            right = packet

    if left is not None and right is not None:
        pairs.append((left, right))
    return pairs


def is_correct_order(left, right):
    if type(left) is int and type(right) is int:
        if left < right:
            return True
        elif left > right:
            return False
        return None
    elif type(left) is list and type(right) is list:
        count = max(len(left), len(right))
        for i in range(count):
            try:
                first = left[i] if len(left) > i else None
                second = right[i] if len(right) > i else None
                if first is None and second is not None:
                    return True
                elif second is None and first is not None:
                    return False
                compare = is_correct_order(first, second)
                if compare is not None:
                    return compare
            except:
                raise
        return None

    list_left = left if type(left) is list else [left]
    list_right = right if type(right) is list else [right]
    return is_correct_order(list_left, list_right)


def cmp_packets(left, right):
    cmp = is_correct_order(left, right)
    if cmp is True:
        return -1
    elif cmp is False:
        return 1
    return 0


def find_correct_pairs(pairs):
    correct = []
    for (i, pair) in enumerate(pairs):
        if is_correct_order(*pair):
            correct.append(i)
    return correct


def part1(lines):
    pairs = parse_pairs(lines)
    correct = find_correct_pairs(pairs)
    return sum(i+1 for i in correct)


def part2(lines):
    divider = [[[2]], [[6]]]
    pairs = parse_pairs(lines)
    packets = []
    packets.extend(divider)
    for pair in pairs:
        packets.extend(pair)
    sorted_packets = sorted(packets, key=cmp_to_key(cmp_packets))

    found = []
    for i, packet in enumerate(sorted_packets):
        if packet in divider:
            found.append(i+1)

    a, b = found
    return a * b


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

