#!/usr/bin/env python3

import sys


def positions(width, height):
    for y in range(height):
        for x in range(width):
            yield (x, y)


class Trees:
    def __init__(self, lines):
        self._height = 0
        self._rows = []
        self._vis_rows = []
        self._scenic_rows = []
        for line in lines:
            line = line.strip()
            if not line:
                break
            row = [int(n) for n in line]
            width = len(row)
            vis_row = [False] * width
            self._width = width
            self._rows.append(row)
            self._vis_rows.append(vis_row)
            self._height += 1

        self.process()

    def width(self):
        return self._width

    def height(self):
        return self._height

    def scenic_score(self, pos):
        x, y = pos
        if x < 1 or x >= self._width - 1:
            return 0
        if y < 1 or y >= self._height - 1:
            return 0

        top, left, right, bottom = 0, 0, 0, 0
        current = self._rows[y][x]

        for dy in range(y - 1, -1, -1):
            tile = self._rows[dy][x]
            top += 1
            if tile >= current:
                break
        for dy in range(y + 1, self._height):
            tile = self._rows[dy][x]
            bottom += 1
            if tile >= current:
                break
        for dx in range(x - 1, -1, -1):
            tile = self._rows[y][dx]
            left += 1
            if tile >= current:
                break
        for dx in range(x + 1, self._width):
            tile = self._rows[y][dx]
            right += 1
            if tile >= current:
                break

        return top * left * right * bottom

    def visibility(self, pos):
        x, y = pos
        return self._vis_rows[y][x]

    def count_visible(self):
        return sum(1 if self.visibility(pos) else 0 for pos in positions(self._width, self._height))

    def max_scenic_score(self):
        max_score = 0
        for pos in positions(self._width, self._height):
            max_score = max(max_score, self.scenic_score(pos))
        return max_score

    def process(self):
        for y, row in enumerate(self._rows):
            prev_max_height = None
            prev_height = None
            for x, height in enumerate(row):
                if x == 0 or prev_max_height < height:
                    self._vis_rows[y][x] = True
                    prev_max_height = height

            prev_max_height = None
            prev_height = None
            for rx, height in enumerate(reversed(row)):
                x = self._width - rx - 1
                if rx == 0 or prev_max_height < height:
                    self._vis_rows[y][x] = True
                    prev_max_height = height

        for x in range(self._width):
            prev_max_height = None
            prev_height = None
            for y in range(self._height):
                height = self._rows[y][x]
                if y == 0 or prev_max_height < height:
                    self._vis_rows[y][x] = True
                    prev_max_height = height

            prev_max_height = None
            prev_height = None
            for ry in range(self._height):
                y = self._height - ry - 1
                height = self._rows[y][x]
                if ry == 0 or prev_max_height < height:
                    self._vis_rows[y][x] = True
                    prev_max_height = height



def part1(lines):
    trees = Trees(lines)
    return trees.count_visible()


def part2(lines):
    trees = Trees(lines)
    return trees.max_scenic_score()


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

