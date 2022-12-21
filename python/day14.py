#!/usr/bin/env python3

import sys
import enum
from collections import defaultdict


def parse_points(line):
    a, b = line.split(',')
    return int(a), int(b)


class Block(enum.Enum):
    Rock = '#'
    Air = '.'
    Sand = 'o'


class Scan:
    def __init__(self, lines):
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        self._blocks = {}
        for line in lines:
            line = line.strip()
            if not line:
                break
            points = [parse_points(p) for p in line.split(' -> ')]
            for i in range(len(points)-1):
                p1 = points[i]
                p2 = points[i + 1]

                min_x = min(min_x, p1[0], p2[0])
                min_y = min(min_y, p1[1], p2[1])
                max_x = max(max_x, p1[0], p2[0])
                max_y = max(max_y, p1[1], p2[1])

                self._plot_line(p1, p2, Block.Rock)

        min_y = 0
        self.bounds = (min_x, min_y, max_x, max_y)
        self._floor = None

    def _plot_line(self, p1, p2, block):
        x1, y1 = p1
        x2, y2 = p2
        dx = (x2 - x1)//abs(x2 - x1) if x2 - x1 != 0 else 0
        dy = (y2 - y1)//abs(y2 - y1) if y2 - y1 != 0 else 0

        if dx != 0:
            for x in range(x1, x2 + dx, dx):
                pos = (x, y1)
                self.set_block(pos, block)

        elif dy != 0:
            for y in range(y1, y2 + dy, dy):
                pos = (x1, y)
                self.set_block(pos, block)

    def set_block(self, pos, block):
        self._blocks[pos] = block

    def get_block(self, pos):
        x, y = pos
        if self._floor is not None and y >= self._floor:
            return Block.Rock
        if pos in self._blocks:
            return self._blocks
        return Block.Air

    def is_out_of_bounds(self, pos):
        x, y = pos
        min_x, min_y, max_x, max_y = self.bounds
        return y > max_y

    def simulate_sand(self, starting_pos):
        sand = starting_pos
        stopped = False
        while not stopped:
            if self.is_out_of_bounds(sand):
                return None
            x, y = sand
            bottom = (x, y+1)
            if self.get_block(bottom) == Block.Air:
                sand = bottom
                continue
            left = (x-1, y+1)
            if self.get_block(left) == Block.Air:
                sand = left
                continue
            right = (x+1, y+1)
            if self.get_block(right) == Block.Air:
                sand = right
                continue
            stopped = True
        self.set_block(sand, Block.Sand)
        return sand

    def set_floor(self, y):
        min_x, min_y, max_x, max_y = self.bounds
        max_y = max(max_x, y)
        self.bounds = (min_x, min_y, max_x, max_y)
        self._floor = y

    def __repr__(self):
        min_x, min_y, max_x, max_y = self.bounds
        rows = []
        for y in range(min_y, max_y+1):
            row = []
            for x in range(min_x, max_x+1):
                pos = (x, y)
                row.append(self.get_block(pos).value)
            rows.append(''.join(row))
        return '\n'.join(rows)


def part1(lines):
    scan = Scan(lines)
    counter = 0
    while True:
        pos = scan.simulate_sand((500, 0))
        if pos is None:
            break
        counter += 1
        #print(scan)
    return counter


def part2(lines):
    scan = Scan(lines)
    _, _, _, max_y = scan.bounds
    scan.set_floor(max_y + 2)
    counter = 0
    start = (500, 0)
    while True:
        pos = scan.simulate_sand(start)
        if pos is None:
            break
        counter += 1
        #print(scan)
        if pos == start:
            break
    return counter


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

