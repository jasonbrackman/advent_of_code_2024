from collections import deque
from functools import lru_cache
from typing import Iterator

import aoc
from aoctypes import Vec2


def parse(path: str):
    lines = aoc.lines(path)
    designs = [a.strip() for a in next(lines).split(",")]
    patterns = [l for l in lines if l]
    return designs, patterns


@lru_cache(maxsize=None)
def possible(filtered: tuple[str, ...], goal: str) -> bool:
    if goal == "":
        return True

    for f in filtered:
        if goal.startswith(f):
            if possible(filtered, goal[len(f) :]):
                return True

    return False


@lru_cache(maxsize=None)
def possibles(filtered: tuple[str, ...], goal: str):
    if goal == "":
        yield True

    for f in filtered:
        if goal.startswith(f):
            yield from possibles(filtered, goal[len(f) :])

    return False


def part01(data):
    c = 0
    designs, patterns = data

    for pattern in patterns:
        filtered = [d for d in designs if d in pattern]
        c += possible(tuple(filtered), pattern)

    assert c == 260


def part02(data):
    c = 0
    designs, patterns = data

    for pattern in patterns:

        filtered = [d for d in designs if d in pattern]
        n = [1 for p in possibles(tuple(filtered), pattern) if p is True]
        print("PATTERN:", pattern, sum(n))
        c += sum(n)

    print(c)


def run():
    path = r"./data/day19.txt"
    data = parse(path)
    part01(data)
    # part02(data)


if __name__ == "__main__":
    run()
