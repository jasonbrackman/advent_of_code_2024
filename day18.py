from collections import deque
from typing import Iterator, Optional

import aoc
from aoctypes import Vec2


def parse(path: str) -> list[Vec2]:
    nums: list[Vec2] = []
    lines = aoc.lines(path)
    for line in lines:
        nums.append(Vec2(aoc.re_ints(line)))
    return nums


def neighbours(node: Vec2, blocks: list[Vec2], grid_length: int) -> Iterator[Vec2]:
    for d in aoc.DIRS:
        t = aoc.add(node, d)
        if 0 <= t[0] < grid_length and 0 <= t[1] < grid_length and t not in blocks:
            yield t


def part01(nums: list[Vec2]) -> Optional[int]:
    grid_length = 71
    data_length = 1024
    v = {(0, 0)}
    q = deque([((0, 0), 0)])
    while q:
        n, c = q.popleft()

        if n == (grid_length - 1, grid_length - 1):
            return c

        for new in neighbours(n, nums[0:data_length], grid_length):
            if new not in v:
                v.add(new)
                q.append((new, c + 1))


def part02(nums: list[Vec2], data_length: int) -> Optional[int]:
    grid_length = 71

    v = {(0, 0)}
    q = deque([((0, 0), 0)])
    while q:
        n, c = q.popleft()

        if n == (grid_length - 1, grid_length - 1):
            return c

        for new in neighbours(n, nums[0:data_length], grid_length):
            if new not in v:
                v.add(new)
                q.append((new, c + 1))


def run() -> None:
    path = r"./data/day18t.txt"
    nums = parse(path)

    assert part01(nums) == 290

    for i in range(len(nums), -1, -1):
        r = part02(nums, i)
        if r is not None:
            assert nums[i] == (64, 54)
            break


if __name__ == "__main__":
    run()
