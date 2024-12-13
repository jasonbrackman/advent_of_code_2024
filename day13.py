import sys
from collections import deque
from dataclasses import dataclass
from turtle import Vec2D

import aoc
from aoctypes import Vec2

"""
3 tokesn to push button a
1 token for button b

"""


@dataclass
class Game:
    a: Vec2
    b: Vec2
    p: Vec2


def parse(path) -> list[Game]:
    goals = []
    lines = aoc.lines(path)
    items = []
    for line in lines:
        nums = aoc.re_ints(line)
        if nums:
            items.append(tuple(nums))
        else:
            goals.append(Game(items[0], items[1], items[2]))
            items.clear()
    if items:
        goals.append(Game(items[0], items[1], items[2]))
    return goals


def equal(p1: Vec2, p2: Vec2) -> bool:
    return p1[0] == p2[0] and p1[1] == p2[1]


def greater(p1: Vec2, p2: Vec2) -> bool:
    return p1[0] > p2[0] or p1[1] > p2[1]


def add(p1: Vec2, p2: Vec2) -> Vec2:
    return p1[0] + p2[0], p1[1] + p2[1]


# 10_000_000_000_000??
def part01(goals: list[Game]) -> int:
    totals = []
    for goal in goals:
        t = {"a": sys.maxsize, "b": sys.maxsize}
        s = (0, 0, (0, 0))
        q = deque([s])
        seen = {s}
        while q:
            a, b, p1 = q.popleft()

            if greater(p1, goal.p):
                continue

            if equal(p1, goal.p):
                if sum((a, b)) < sum(t.values()):
                    t["a"] = a
                    t["b"] = b
                continue

            newa = a + 3, b, add(p1, goal.a)
            newb = a, b + 1, add(p1, goal.b)
            for item in (newa, newb):
                if item not in seen:
                    seen.add(item)
                    q.append(item)
        final = (t["a"], t["b"])
        if not equal(final, (sys.maxsize, sys.maxsize)):
            totals.append(sum(final))

    return sum(totals)


def run() -> None:
    path = r"./data/day13.txt"  # not 28678
    goals = parse(path)
    assert part01(goals) == 29023


if __name__ == "__main__":
    run()
