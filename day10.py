from typing import Iterator

import aoc
from collections import deque

from aoc import Grid, Vec2

dirs = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)


def parse(path: str) -> Grid:
    grid = []
    for line in aoc.lines(path):
        grid.append([int(i) for i in line])
    return grid


def part01(grid: Grid, positions: list[Vec2]) -> int:
    t = 0
    for pos in positions:
        found = set()
        visited = {(0, pos)}
        q = deque([(0, pos)])
        while q:
            (val, pos) = q.popleft()
            if val == 9:
                found.add(pos)
                continue
            for n in get_next(grid, val, pos):
                if n not in visited:
                    visited.add((val + 1, n))
                    q.append((val + 1, n))
        t += len(found)
    return t


def part02(grid: Grid, positions: list[Vec2]) -> int:
    t = 0
    for pos in positions:
        found = []
        q = deque([(0, pos)])
        while q:
            (val, pos) = q.popleft()
            if val == 9:
                found.append(pos)
                continue
            for n in get_next(grid, val, pos):
                q.append((val + 1, n))
        t += len(found)

    return t


def get_next(grid: Grid, val: int, p1: Vec2) -> Iterator[Vec2]:
    for p2 in dirs:
        y, x = p1[0] + p2[0], p1[1] + p2[1]
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            new_val = grid[y][x]
            if new_val != "." and new_val == val + 1:
                yield y, x


def get_start_pos(grid: Grid) -> Iterator[Vec2]:
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] == 0:
                yield j, i


def run() -> None:
    path = r"./data/day10.txt"
    grid = parse(path)
    positions = list(get_start_pos(grid))
    assert part01(grid, positions) == 798
    assert part02(grid, positions) == 1816


if __name__ == "__main__":
    run()
