from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Optional

import aoc
from aoc import DIRS, add
from aoctypes import Grid, Vec2


@dataclass
class Node:
    pos: Vec2
    value: int
    parent: Optional["Node"] = None


def parse(path: str) -> Grid:
    return aoc.grid(path)


def get_item(grid: Grid, needle: str) -> Vec2:
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] == needle:
                return j, i
    raise ValueError


def track_path(grid: Grid, start: Vec2, goal: Vec2) -> Node:
    q: deque[Node] = deque([Node(start, 0, None)])
    v = {
        start,
    }
    while q:

        node = q.popleft()

        if node.pos == goal:
            return node

        for d in DIRS:
            np = add(node.pos, d)
            if np in v:
                continue

            v.add(np)
            y, x = np
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                is_wall = grid[np[0]][np[1]] == "#"
                if not is_wall:
                    q.append(Node(np, node.value + 1, parent=node))

    raise ValueError


def collect_cheat_values(positions: dict[Vec2, int]) -> defaultdict[int, int]:
    results: defaultdict[int, int] = defaultdict(int)
    for k, v in reversed(positions.items()):
        for d in DIRS:

            # move once
            np = add(k, d)
            if np in positions:
                continue

            # move a second time
            np = add(np, d)
            if np in positions:
                if positions[np] > v:
                    # let's calculate the change, if any
                    results[positions[np] - v - 2] += 1
    return results


def get_positions(node: Optional[Node]) -> dict[Vec2, int]:
    positions: dict[Vec2, int] = {}
    while node:
        positions[node.pos] = node.value
        node = node.parent
    return positions


def run() -> None:
    path = r"./data/day20.txt"
    grid = parse(path)
    start = get_item(grid, "S")
    goal = get_item(grid, "E")

    # part01
    node = track_path(grid, start, goal)
    positions = get_positions(node)
    results = collect_cheat_values(positions)

    t = 0
    for k, v in results.items():
        if k >= 100:
            t += v
    assert t == 1378


if __name__ == "__main__":
    run()
