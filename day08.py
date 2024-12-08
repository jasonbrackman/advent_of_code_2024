from collections import defaultdict
from itertools import combinations

import aoc
from aoc import Grid

Vec2 = tuple[int, int]
Antennas = defaultdict[str, set[Vec2]]


def part01(grid: Grid) -> int:
    h, w = len(grid), len(grid[0])
    locs = _locs(grid)

    nodes = {
        item
        for j in locs.values()
        for p1, p2 in combinations(j, 2)
        for dist in [_sub(p1, p2)]
        for item in (_add(p1, dist), _sub(p1, dist), _add(p2, dist), _sub(p2, dist))
        if item not in (p1, p2) and _in_grid(item, h, w)
    }
    return len(nodes)


def part02(grid: Grid) -> int:
    h, w = len(grid), len(grid[0])
    locs = _locs(grid)

    nodes = set()
    for k, j in locs.items():
        for p1, p2 in combinations(j, 2):
            # Add the two antennas directly
            nodes.update([p1, p2])

            # Calculate the distance vector
            dist = _sub(p1, p2)

            # Propagate signals in both directions
            for direction in (_add, _sub):
                pos = direction(p1, dist)
                while _in_grid(pos, h, w):
                    nodes.add(pos)
                    pos = direction(pos, dist)

    return len(nodes)


def _locs(grid: Grid) -> Antennas:
    # get the width height and locations of antennas on the grid
    locs = defaultdict(set)
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] != ".":
                locs[grid[j][i]].add((j, i))
    return locs


def _add(p1: Vec2, p2: Vec2) -> Vec2:
    return p1[0] + p2[0], p1[1] + p2[1]


def _sub(p1: Vec2, p2: Vec2) -> Vec2:
    return p1[0] - p2[0], p1[1] - p2[1]


def _in_grid(p: Vec2, h: int, w: int) -> bool:
    return 0 <= p[0] < h and 0 <= p[1] < w


def run() -> None:
    path = r"./data/day08.txt"
    grid = aoc.grid(path)
    assert part01(grid) == 398
    assert part02(grid) == 1333


if __name__ == "__main__":
    run()
