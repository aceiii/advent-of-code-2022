#!/usr/bin/env python3

import sys


def move(pos, direction):
    x, y = pos
    if direction == 'R':
        x += 1
    elif direction == 'L':
        x -= 1
    elif direction == 'U':
        y += 1
    else:
        y -= 1
    return (x, y)


def follow(current, towards):
    x1, y1 = current
    x2, y2 = towards
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > 1:
        x1 += dx//abs(dx)
        if abs(dy) > 0:
            y1 += dy//abs(dy)
    elif abs(dy) > 1:
        y1 += dy//abs(dy)
        if abs(dx) > 0:
            x1 += dx//abs(dx)
    return (x1, y1)


def part1(lines):
    head = (0, 0)
    tail = (0, 0)
    visited = set([tail])
    for line in lines:
        direction, steps = line.strip().split()
        steps = int(steps)
        for _ in range(steps):
            head = move(head, direction)
            tail = follow(tail, head)
            visited.add(tail)
    return len(visited)


def part2(lines):
    n = 10
    knots =  [(0,0)] * n
    visited = set([(0,0)])
    for line in lines:
        direction, steps = line.strip().split()
        steps = int(steps)
        for _ in range(steps):
            for idx in range(n):
                knot = knots[idx]
                if idx == 0:
                    knot = move(knot, direction)
                else:
                    knot = follow(knot, knots[idx - 1])
                knots[idx] = knot
                if idx == n-1:
                    visited.add(knot)
    return len(visited)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

