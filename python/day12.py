#!/usr/bin/env python3

import sys
import string
import heapq
from collections import defaultdict


def map_height(letter):
    return string.ascii_lowercase.find(letter)


def parse_heightmap(lines):
    rows = []
    start = None
    end = None
    height = 0
    width = 0
    y = 0

    for line in lines:
        line = line.strip()
        if not line:
            break

        width = len(line)
        height += 1
        row = []

        for (x, c) in enumerate(line):
            pos = (x, y)
            if c == 'S':
                row.append(0)
                start = pos
            elif c == 'E':
                row.append(25)
                end = pos
            else:
                row.append(map_height(c))

        rows.append(row)
        y += 1

    return {
        'width': width,
        'height': height,
        'grid': rows,
        'start': start,
        'end': end,
    }


class Graph:
    class Tile:
        def __init__(self, pos):
            self.pos = pos
            self.next = []

        def __repr__(self):
            pos = str(self.pos)
            next = ', '.join(str(n.pos) for n in self.next)
            return f'{pos} -> {next}'

    def __init__(self):
        self._tiles = {}

    def get(self, key):
        if key not in self._tiles:
            self._tiles[key] = Graph.Tile(key)
        return self._tiles[key]

    def tiles(self):
        return self._tiles.values()

    def __str__(self):
        return '\n'.join(str(tile) for tile in self._tiles.values())


def gen_graph(grid, width, height):
    graph = Graph()
    for (y, row) in enumerate(grid):
        for (x, val) in enumerate(row):
            pos = (x, y)
            top = ((x, y-1), grid[y-1][x]) if y > 0 else None
            bottom = ((x, y+1), grid[y+1][x]) if y < height-1 else None
            left = ((x-1, y), grid[y][x-1]) if x > 0 else None
            right = ((x+1, y), grid[y][x+1]) if x < width-1 else None

            tile = graph.get(pos)

            if top is not None and top[1] <= val+1:
                tile.next.append(graph.get(top[0]))
            if bottom is not None and bottom[1] <= val+1:
                tile.next.append(graph.get(bottom[0]))
            if left is not None and left[1] <= val+1:
                tile.next.append(graph.get(left[0]))
            if right is not None and right[1] <= val+1:
                tile.next.append(graph.get(right[0]))

    return graph


def shortest_path(graph, start):
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    visited = defaultdict(lambda: False)
    queue = [(dist[tile.pos], tile.pos) for tile in graph.tiles()]
    heapq.heapify(queue)
    while queue:
        _, pos = heapq.heappop(queue)
        tile = graph.get(pos)
        visited[tile.pos] = True

        for next_tile in tile.next:
            if visited[next_tile.pos]:
                continue
            new_dist = dist[tile.pos] + 1
            if new_dist < dist[next_tile.pos]:
                dist[next_tile.pos] = new_dist

        queue = [(dist[tile.pos], tile.pos) for tile in graph.tiles() if not visited[tile.pos]]
        heapq.heapify(queue)

    return dist


def find_lowest_points(grid):
    lowest = []
    for (y, row) in enumerate(grid):
        for (x, height) in enumerate(row):
            pos = (x, y)
            if height == 0:
                lowest.append(pos)
    return lowest


def reverse_graph(graph):
    rgraph = Graph()
    for tile in graph.tiles():
        new_tile = rgraph.get(tile.pos)
        for next_tile in tile.next:
            new_next_tile = rgraph.get(next_tile.pos)
            new_next_tile.next.append(new_tile)
    return rgraph


def part1(lines):
    hm = parse_heightmap(lines)
    graph = gen_graph(hm['grid'], hm['width'], hm['height'])
    dist = shortest_path(graph, hm['start'])
    return dist[hm['end']]


def part2(lines):
    hm = parse_heightmap(lines)
    graph = reverse_graph(gen_graph(hm['grid'], hm['width'], hm['height']))
    dist = shortest_path(graph, hm['end'])
    starting = find_lowest_points(hm['grid'])
    min_path = float('inf')
    for pos in starting:
        min_path = min(min_path, dist[pos])
    return min_path


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

