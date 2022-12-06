#!/usr/bin/env python3

import sys
import re
from collections import defaultdict


def group_lines(lines):
    groups = []
    group = []
    for line in lines:
        if not line.strip():
            groups.append(group)
            group = []
            continue
        group.append(line.strip("\n"))
    if group:
        groups.append(group)
    return groups


def parse_input(lines):
    stack_lines, move_lines = group_lines(lines)
    stacks = defaultdict(lambda: [])
    moves = []

    for line in stack_lines:
        line = line.strip("\n")
        if not line:
            break
        for idx in range(0, len(line), 4):
            part = line[idx:idx+4][1:2].strip()
            if not part or str.isdigit(part):
                continue
            stacks[(idx//4)+1].append(part)

    for line in move_lines:
        line = line.strip()
        if not line:
            break
        moves.append([int(i) for i in re.sub("[^0-9 ]", "", line).strip().split()])

    for key in stacks.keys():
        stacks[key] = list(reversed(stacks[key]))

    return stacks, moves


def perform_move(stacks, from_idx, to_idx):
    item = stacks[from_idx].pop()
    stacks[to_idx].append(item)


def perform_stacked_move(stacks, move):
    count, from_idx, to_idx = move
    temp_stack = []
    for _ in range(count):
        item = stacks[from_idx].pop()
        temp_stack.append(item)
    while temp_stack:
        stacks[to_idx].append(temp_stack.pop())


def run_moves(stacks, moves):
    for (count, from_idx, to_idx) in moves:
        for _ in range(count):
            perform_move(stacks, from_idx, to_idx)


def run_moves2(stacks, moves):
    for move in moves:
        perform_stacked_move(stacks, move)


def part1(lines):
    stacks, moves = parse_input(lines)
    run_moves(stacks, moves)
    result = [stacks[key][-1] for key in sorted(stacks.keys())]
    return "".join(result)



def part2(lines):
    stacks, moves = parse_input(lines)
    run_moves2(stacks, moves)
    result = [stacks[key][-1] for key in sorted(stacks.keys())]
    return "".join(result)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

