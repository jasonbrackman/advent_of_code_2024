from collections import defaultdict

import aoc
from aoctypes import Vec2, Grid

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def parse(path: str) -> Grid:
    grid = aoc.grid(path)
    return grid


def add_points(p1: Vec2, p2: Vec2) -> Vec2:
    return p1[0] + p2[0], p1[1] + p2[1]


def get_value(p1: Vec2, grid: Grid) -> str:
    return grid[p1[0]][p1[1]]


def on_grid(p1: Vec2, grid: Grid) -> bool:
    return 0 <= p1[0] < len(grid) and 0 <= p1[1] < len(grid[0])


def find_area(p1: Vec2, grid: Grid) -> set[Vec2]:
    v = get_value(p1, grid)
    result = {p1}
    s = {p1}
    q = [p1]
    while q:
        a = q.pop()
        for b in DIRS:

            p3 = add_points(a, b)
            if on_grid(p3, grid):
                if p3 not in s:
                    s.add(p3)
                    if get_value(p3, grid) == v:
                        result.add(p3)
                        q.append(p3)
    return result


# def in_area(p1, amax_, amin_, bmax_, bmin_):
#     if amin_ < p1[0] <= amax_ and bmin_ < p1[1] <= bmax_:
#         return True
#     return False


def part01(grid: Grid) -> int:
    areas = defaultdict(list)
    seen: set[Vec2] = set()

    # find areas
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if (j, i) not in seen:
                r = find_area((j, i), grid)
                areas[get_value((j, i), grid)].append(r)
                seen |= r

    # calculate Fencing cost
    t = 0
    for k, v in areas.items():
        for a in v:
            p = get_perimeter(a)

            r = p * len(a)
            t += r
    return t


def get_perimeter(points: list[Vec2]) -> int:
    t = 0
    for p1 in points:
        for d in DIRS:
            p2 = add_points(p1, d)
            if p2 not in points:
                t += 1
    return t


def run() -> None:
    path = r"./data/day12.txt"  # 73442192 too high
    grid = parse(path)
    assert part01(grid) == 1319878


if __name__ == "__main__":
    run()
