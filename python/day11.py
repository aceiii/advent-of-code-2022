#!/usr/bin/env python3

import sys


funcs = {
    '*': lambda a,b: a * b,
    '+': lambda a,b: a + b,
    '-': lambda a,b: a - b,
}


def parse_value(val, orig_value):
    if val == 'old':
        return orig_value
    return int(val)


def parse_operation(op):
    left, mid, right = op.split()

    def op_func(x):
        a = parse_value(left, x)
        b = parse_value(right, x)
        func = funcs[mid]
        return func(a, b)

    return op_func


def parse_notes(lines):
    notes = []
    note = None
    for line in lines:
        line = line.strip()
        if not line:
            notes.append(note)
            note = None
            continue
        if note is None:
            note = {}

        if line.find('Monkey ') == 0:
            note['id'] = int(line[7:-1])
        elif line.find('Starting items: ') == 0:
            note['items'] = [int(x.strip()) for x in line[16:].split(',')]
        elif line.find('Operation: new = ') == 0:
            note['op'] = parse_operation(line[17:].strip())
        elif line.find('Test: divisible by ') == 0:
            div = int(line[19:].strip())
            note['test'] = div
        elif line.find('If true: throw to monkey ') == 0:
            monkey = int(line[25:].strip())
            note['if_true'] = monkey
        elif line.find('If false: throw to monkey ') == 0:
            monkey = int(line[26:].strip())
            note['if_false'] = monkey

    if note is not None:
        notes.append(note)

    return notes


class Monkey:
    def __init__(self, note):
        self._id = note['id']
        self._test = note['test']
        self._op = note['op']
        self._items = note['items'][:]
        self._true = note['if_true']
        self._false = note['if_false']

    def __str__(self):
        items = ', '.join(str(x) for x in self._items)
        return f"Monkey {str(self._id)}: {items}"

    def op(self, value, relief_op):
        new_value = self._op(value)
        if relief_op is not None:
            new_value = relief_op(new_value)
        return new_value

    def test(self, value):
        return self._true if value % self._test == 0 else self._false

    def push_item(self, item):
        self._items.append(item)

    def step(self, relief_op=None):
        while self._items:
            orig_value = self._items.pop(0)
            value = self.op(orig_value, relief_op)
            yield (self.test(value), value)


class Monkeys:
    def __init__(self, notes):
        self._monkeys = []
        self._inspected = []
        self._relief_op = None
        for note in notes:
            self._monkeys.append(Monkey(note))
            self._inspected.append(0)

    def configure_relief(self, relief_op):
        self._relief_op = relief_op

    def round(self):
        for (idx, monkey) in enumerate(self._monkeys):
            for (to_monkey, value) in monkey.step(self._relief_op):
                self._monkeys[to_monkey].push_item(value)
                self._inspected[idx] += 1

    def __str__(self):
        return '\n'.join(str(monkey) for monkey in self._monkeys)

    def monkey_business(self):
        [a, b, *rest] = sorted(self._inspected, reverse=True)
        return a * b


def part1(lines):
    notes = parse_notes(lines)
    monkeys = Monkeys(notes)
    monkeys.configure_relief(lambda x: int(x / 3))
    for _ in range(20):
        monkeys.round()
    return monkeys.monkey_business()


def part2(lines):
    notes = parse_notes(lines)
    monkeys = Monkeys(notes)
    multiple = 1
    for note in notes:
        multiple = multiple * note['test']
    monkeys.configure_relief(lambda x: x % multiple)
    for _ in range(10000):
        monkeys.round()
    return monkeys.monkey_business()


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

