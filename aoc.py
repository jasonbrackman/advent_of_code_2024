import math
import sys
import time
from pathlib import Path
from typing import Iterator, Union, Callable
import re

from aoctypes import Grid, Vec2

sys.setrecursionlimit(1_000_000)

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))

NUM_PATTERN = re.compile(r"-?\d+")
WRD_PATTERN = re.compile(r"[a-zA-Z]+")


class AOCException(Exception):
    pass


def grid(path: Union[Path, str]) -> Grid:
    return [list(line) for line in lines(path)]


def lines(path: Union[Path, str]) -> Iterator[str]:
    with open(path, encoding="utf8") as handle:
        for line in handle:
            yield line.strip()


def ints(path: Union[Path, str]) -> Iterator[list[int]]:
    for line in lines(path):
        yield re_ints(line)


def re_nums(s: str) -> list[str]:
    return re.findall(NUM_PATTERN, s)


def re_ints(s: str) -> list[int]:
    """Search for numbers in text and returns them as ints. If a number
    has consecutive digits beside each other they are considered one number:
    001 = [int(1)]
    2asdf2 = [int(2), int(2)]
    asdf45asdf = [int(45)]
    -1, 45, -5 = [int(-1), int(45), int(-5)]
    """
    return [int(ii) for ii in list(re_nums(s))]


def re_wrds(s: str) -> list[str]:
    """Search for clusters of uninterrupted text. Will ignore anything
    other than a-zA-Z."""
    return re.findall(WRD_PATTERN, s)


def concat_numbers(a: int, b: int) -> int:
    """Multiply the first number to shift left by the length of the second number.
    Then add them together and return.  Should outperform string conversion and add
    on larger numbers."""
    count = math.floor(math.log10(b)) + 1
    return a * 10**count + b


def add(p1: Vec2, p2: Vec2) -> Vec2:
    return p1[0] + p2[0], p1[1] + p2[1]


def time_it(command: Callable):
    t1 = time.perf_counter()
    command()
    print(
        f"[{str(command.__module__)}.{command.__name__}]: Completed in {(time.perf_counter() - t1)*1_000:0.1f} ms"
    )


def time_it_all(args: list[Callable]):
    for arg in args:
        time_it(arg)
