from typing import Optional
import heapq

import aoc
from aoctypes import Vec2, Grid


def parse(path: str) -> Grid:
    grid = aoc.grid(path)

    return grid


def get_start(grid: Grid) -> Vec2:
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] == "S":
                return j, i
    raise ValueError


def add(p1: Vec2, p2: Vec2) -> Vec2:
    y, x = p1
    yy, xx = p2
    return y + yy, x + xx


def neighbours(p1: Vec2) -> list[tuple[Vec2, Vec2]]:
    dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    r = []
    for d in dirs:
        yy, xx = add(p1, d)
        # skipping bounds check as its impossible to reach.
        r.append(((yy, xx), d))
    return r


class Node:
    def __init__(self, p: Vec2, d: Vec2, v: int, parent: Optional["Node"] = None):
        self.pos = p
        self.dir = d
        self.val = v
        self.parent = parent

    def __lt__(self, other: "Node"):
        return self.val < other.val


def parts(grid: Grid) -> list[Node]:

    # return results
    t: list[Node] = []

    # Create priority queue
    pq: list[Node] = []
    heapq.heappush(pq, Node(get_start(grid), (0, 1), 0, parent=None))

    # shortcut if we can
    visited: dict[tuple[Vec2, Vec2], int] = {}

    while pq:
        node = heapq.heappop(pq)

        if grid[node.pos[0]][node.pos[1]] == "E":
            t.append(node)
            continue

        for new, newd in neighbours(node.pos):
            move_cost = (
                1 if node.dir == newd else 1001
            )  # 1001 to cover cost of `turn` and `move`

            if (new, newd) in visited and visited[(new, newd)] < node.val + move_cost:
                continue
            visited[(new, newd)] = node.val + move_cost

            if grid[new[0]][new[1]] == "#":
                # no walls
                continue

            heapq.heappush(pq, Node(new, newd, node.val + move_cost, parent=node))

    return t


def path_positions(node: Node) -> set[Vec2]:
    s = set()
    while node.parent:
        s.add(node.pos)
        node = node.parent
    s.add(node.pos)
    return s


def run() -> None:
    path = r"./data/day16.txt"
    grid = parse(path)
    vals = parts(grid)
    assert vals[0].val == 111480
    p2 = set()
    for val in vals:
        p2 |= path_positions(val)
    assert len(p2) == 529


if __name__ == "__main__":
    run()
