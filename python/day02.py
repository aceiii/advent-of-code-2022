#!/usr/bin/env python3

import sys
from enum import IntEnum


class Outcome(IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


class Shape(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def oponent_hand(hand):
    if hand == 'A':
        return Shape.ROCK
    elif hand == 'B':
        return Shape.PAPER
    else:
        return Shape.SCISSORS


def player_hand(hand):
    if hand == 'X':
        return Shape.ROCK
    elif hand == 'Y':
        return Shape.PAPER
    else:
        return Shape.SCISSORS


def player_outcome(outcome):
    if outcome == 'X':
        return Outcome.LOSS
    elif outcome == 'Y':
        return Outcome.DRAW
    else:
        return Outcome.WIN


def check_hands(oponent, player):
    if oponent == player:
        return Outcome.DRAW
    if oponent == Shape.ROCK and player == Shape.SCISSORS:
        return Outcome.LOSS
    elif player == Shape.ROCK and oponent == Shape.SCISSORS:
        return Outcome.WIN
    elif oponent == Shape.PAPER and player == Shape.ROCK:
        return Outcome.LOSS
    elif player == Shape.PAPER and oponent == Shape.ROCK:
        return Outcome.WIN
    elif oponent == Shape.SCISSORS and player == Shape.PAPER:
        return Outcome.LOSS
    else:
        return Outcome.WIN


def hand_from_outcome(oponent, outcome):
    if outcome == Outcome.DRAW:
        return oponent

    if oponent == Shape.ROCK:
        if outcome == Outcome.WIN:
            return Shape.PAPER
        else:
            return Shape.SCISSORS
    elif oponent == Shape.PAPER:
        if outcome == Outcome.WIN:
            return Shape.SCISSORS
        else:
            return Shape.ROCK
    else:
        if outcome == Outcome.WIN:
            return Shape.ROCK
        else:
            return Shape.PAPER


def part1(lines):
    total_score = 0
    for line in lines:
        a, b = line.strip().split(' ')
        oponent = oponent_hand(a)
        player = player_hand(b)
        outcome = check_hands(oponent, player)
        total_score += int(player) + int(outcome)
    return total_score


def part2(lines):
    total_score = 0
    for line in lines:
        a, b = line.strip().split(' ')
        oponent = oponent_hand(a)
        outcome = player_outcome(b)
        player = hand_from_outcome(oponent, outcome)
        total_score += int(player) + int(outcome)
    return total_score


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

