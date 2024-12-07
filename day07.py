import operator
from collections import deque
from itertools import product
from typing import Callable

import aoc


def parse(path: str):
    lines = aoc.lines(path)
    return [aoc.re_ints(line) for line in lines]


def glue(a, b) -> int:
    return int(f"{a}{b}")


def is_valid(val: int, rest: list[int], operators: list[Callable]) -> bool:

    ops_combos = product(operators, repeat=len(rest) - 1)

    for ops in ops_combos:
        ii = 0  # ops index
        bucket = []
        temp = deque(rest)  # need a copy / likely slow with all the copy/popping
        while temp:
            # every operator needs a bucket of two items to work on.
            while len(bucket) < 2:
                bucket.append(temp.popleft())

            # bucket contents replaced with new value
            bucket = [ops[ii](*bucket)]

            # a simple optimization attempt
            if temp and bucket[0] > val:
                temp.clear()

            ii += 1  # move ops index forward

        if bucket[0] == val:
            return True
    return False


def part01(data):
    operators = [operator.mul, operator.add]
    t = sum(d[0] for d in data if is_valid(d[0], d[1:], operators))
    assert t == 882304362421


def part02(data):
    operators = [operator.mul, operator.add, glue]
    t = sum(d[0] for d in data if is_valid(d[0], d[1:], operators))
    assert t == 145149066755184


def run():
    path = r"./data/day07.txt"
    data = parse(path)
    part01(data)
    part02(data)


if __name__ == "__main__":
    run()