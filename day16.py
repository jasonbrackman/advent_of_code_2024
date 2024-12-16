from typing import Optional
import heapq

import aoc
from aoctypes import Vec2, Grid


def parse(path):
    grid = aoc.grid(path)

    return grid


def get_start(grid: Grid) -> Vec2:
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] == "S":
                return j, i
    raise ValueError


def add(p1, p2):
    y, x = p1
    yy, xx = p2
    return y + yy, x + xx


def neighbours(p1, grid: Grid):
    dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    r = []
    for d in dirs:
        yy, xx = add(p1, d)
        # skipping bounds check as its impossible to reach.
        r.append(((yy, xx), d))
    return r


class Node:
    def __init__(self, pos: Vec2, dir: Vec2, val: int, parent: Optional["Node"] = None):
        self.pos = pos
        self.dir = dir
        self.val = val
        self.parent = parent

    def __lt__(self, other: "Node"):
        return self.val < other.val


def past(node: Node):

    while node.parent:
        yield node.pos
        node = node.parent


def part01(grid: Grid):
    t = []
    n = get_start(grid)
    pq = []
    heapq.heappush(pq, Node(n, (0, 1), 0, parent=None))
    visited = set()
    while pq:
        node = heapq.heappop(pq)

        y, x = node.pos

        if grid[y][x] == "E":
            return node

        for new, newd in neighbours((y, x), grid):
            move_cost = 1 if node.dir == newd else 1001
            if (new, newd) not in visited:
                visited.add((new, newd))
                if grid[new[0]][new[1]] == "#":
                    continue

                heapq.heappush(pq, Node(new, newd, node.val + move_cost, parent=node))

    return t


def run():
    path = r"./data/day16.txt"  # not 137424
    grid = parse(path)
    p1 = part01(grid)
    assert p1.val == 111488


if __name__ == "__main__":
    run()
