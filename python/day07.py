#!/usr/bin/env python3

import sys


def parse_commands(lines):
    cmds = []
    current_cmd = None
    output = []
    for line in lines:
        line = line.strip()
        if not line:
            break

        parts = line.split()

        if parts[0] == '$':
            if current_cmd is not None:
                cmds.append([current_cmd, output])
                current_cmd = None
                output = []

            current_cmd = parts[1:]
        else:
            output.append(parts)

    if current_cmd is not None:
        cmds.append([current_cmd, output])

    return cmds


def build_full_path(root, name):
    return '/' + (root + '/' + name).strip('/')


class FileSystem:
    def __init__(self, cmds):
        self._paths = {}
        self._paths['/'] = {
            'type': 'dir',
            'full_path': '/',
            'name': '/',
            'size': 0,
            'files': set(),
            'dirs': set(),
            'parent': None,
        }
        current_dir = None
        for ([cmd, *args], output) in cmds:
            if cmd == 'cd' and args == ['/']:
                current_dir = self._paths['/']
            elif cmd == 'cd' and args == ['..']:
                current_dir = current_dir['parent']
            elif cmd == 'cd':
                name = args[0]
                full_path = build_full_path(current_dir['full_path'], name)
                if full_path not in self._paths:
                    self._paths[full_path] = {
                        'type': 'dir',
                        'full_path': full_path,
                        'name': name,
                        'size': 0,
                        'files': set(),
                        'dirs': set(),
                        'parent': current_dir,
                    }
                current_dir = self._paths[full_path]
            elif cmd == 'ls':
                for (dir_or_size, name) in output:
                    full_path = build_full_path(current_dir['full_path'], name)
                    size = 0 if dir_or_size == 'dir' else int(dir_or_size)
                    file_type = 'dir' if dir_or_size == 'dir' else 'file'
                    if full_path not in self._paths:
                        self._paths[full_path] = {
                            'type': file_type,
                            'full_path': full_path,
                            'name': name,
                            'size': size,
                            'files': set(),
                            'dirs': set(),
                            'parent': current_dir,
                        }
                    if file_type == 'dir':
                        current_dir['dirs'].add(name)
                    elif file_type == 'file':
                        current_dir['files'].add(name)

    def get_size(self, full_path):
        path = self._paths[full_path]
        if path is None:
            return 0
        if path['type'] == 'dir':
            total_size = 0
            for name in [*path['files'], *path['dirs']]:
                new_full_path = build_full_path(full_path, name)
                total_size += self.get_size(new_full_path)
            return total_size
        return path['size']

    def get_path_info(self, full_path):
        return self._paths[full_path]

    def recursive_dirs(self):
        paths = ['/']
        while paths:
            path = paths.pop()
            path_info = self.get_path_info(path)
            yield path_info
            if path_info is not None:
                for dir_path in path_info['dirs']:
                    full_path = build_full_path(path, dir_path)
                    paths.append(full_path)


def part1(lines):
    cmds = parse_commands(lines)
    fs = FileSystem(cmds)
    total_size = 0
    for path in fs.recursive_dirs():
        size = fs.get_size(path['full_path'])
        if size <= 100000:
            total_size += size
    return total_size


def part2(lines):
    total_disk_space = 70000000
    required_space = 30000000
    cmds = parse_commands(lines)
    fs = FileSystem(cmds)
    root_size = fs.get_size('/')
    free_space = total_disk_space - root_size
    min_to_free = required_space - free_space
    answer = root_size
    for path in fs.recursive_dirs():
        size = fs.get_size(path['full_path'])
        if path['type'] == 'dir' and size >= min_to_free:
            answer = min(answer, size)
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

