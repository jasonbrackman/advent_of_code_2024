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


def get_areas(grid: Grid) -> list[set[Vec2]]:
    areas: list[set[Vec2]] = []
    seen: set[Vec2] = set()
    # find areas
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if (j, i) not in seen:
                r = find_area((j, i), grid)
                areas.append(r)
                seen |= r
    return areas


def part01(areas: list[set[Vec2]]) -> int:
    # calculate Fencing cost
    t = 0
    for area in areas:
        p = get_perimeter(area)
        t += p * len(area)
    return t


def part02(areas: list[set[Vec2]]) -> int:
    # calculate Fencing cost
    t = 0
    for area in areas:
        p = walk_perimeter(area)
        t += p * len(area)
    return t


def get_perimeter(points: set[Vec2]) -> int:
    t = 0
    for p1 in points:
        for d in DIRS:
            p2 = add_points(p1, d)
            if p2 not in points:
                t += 1
    return t


def walk_perimeter(points: set[Vec2]) -> int:
    r = 0
    for p1 in sorted(points):
        n = 0
        up = add_points(p1, (-1, 0))
        dn = add_points(p1, (1, 0))
        lt = add_points(p1, (0, -1))
        rt = add_points(p1, (0, 1))

        if up not in points:
            if lt not in points or lt in points and add_points(lt, (-1, 0)) in points:
                n += 1
        if dn not in points:
            if lt not in points or lt in points and add_points(lt, (1, 0)) in points:
                n += 1
        if rt not in points:
            if up not in points or up in points and add_points(up, (0, 1)) in points:
                n += 1
        if lt not in points:
            if up not in points or up in points and add_points(up, (0, -1)) in points:
                n += 1

        r += n
    return r


def run() -> None:
    path = r"./data/day12.txt"
    grid = parse(path)
    areas = get_areas(grid)
    assert part01(areas) == 1319878
    assert part02(areas) == 784982


if __name__ == "__main__":
    run()
