import sys

from dataclasses import dataclass
from typing import Optional
import heapq

import aoc
from aoctypes import Vec2, Grid


@dataclass(frozen=True)
class Node:
    pos: Vec2
    dir: str
    depth: int
    idx: int
    parent: Optional["Node"]

    def __lt__(self, other: "Node"):
        return self.depth < other.depth

    def to_string(self):
        r = self
        p = ""
        while r:
            p += r.dir
            r = r.parent
        return p[::-1]


def parse(path):
    lines = aoc.lines(path)
    return [list(line) for line in lines]


DIRS = {
    # y, x
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def search_grid(pos: Vec2, goals: str, grid: Grid, maxsize) -> tuple[int, set[Node]]:

    results = set()
    goal_depth: list[int] = [maxsize] * len(goals)
    pq: list[Node] = []
    heapq.heappush(pq, Node(pos, "", 0, 0, None))

    while pq:
        node = heapq.heappop(pq)

        if node.depth > goal_depth[node.idx]:
            continue

        if grid[node.pos[0]][node.pos[1]] == goals[node.idx]:
            if node.depth < goal_depth[node.idx]:
                goal_depth[node.idx] = node.depth
            new_node = Node(node.pos, "A", node.depth + 1, node.idx + 1, node)

            if new_node.idx == len(goals):
                results.add(new_node)
            else:
                heapq.heappush(pq, new_node)
            continue

        for dir_ in DIRS:
            new_pos = aoc.add(node.pos, DIRS[dir_])
            if node.parent and node.parent.pos == new_pos:
                continue
            y, x = new_pos
            if 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x] != " ":
                heapq.heappush(pq, Node(new_pos, dir_, node.depth + 1, node.idx, node))

    return goal_depth[-1] + 1, results


def part01():
    grid_nums = [
        list("789"),
        list("456"),
        list("123"),
        list(" 0A"),
    ]
    grid_pad = [
        list(" ^A"),
        list("<v>"),
    ]
    # print("Number Pad:")
    # for p in grid_nums:
    #     print(p)
    # print("Controller Pad:")
    # for p in grid_pad:
    #     print(p)
    t = 0
    records = parse(r"./data/day21.txt")
    for goals in records:
        num = aoc.re_ints("".join(goals))[0]

        low, results = search_grid((3, 2), goals, grid_nums, sys.maxsize)
        print(f"Shortest Path Results: '{low}'")

        rounds = [sys.maxsize] * 2
        for index in range(2):
            # max_ = sys.maxsize
            old = set(results)
            new_items = set()
            for node in old:
                if node.depth > rounds[index]:
                    continue
                low, new = search_grid(
                    (0, 2), node.to_string(), grid_pad, rounds[index]
                )
                if low <= rounds[index]:
                    rounds[index] = low
                    new_items |= new

            if new_items:
                print(
                    f"Shortest Path Round {index}: {goals} - '{list(new_items)[0].depth}'"
                )
                results = {n for n in new_items if n.depth == rounds[index]}

        low = sys.maxsize
        for node in results:
            if node.depth < low:
                low = node.depth

        t += num * low
    assert t == 157892


def main():
    part01()


if __name__ == "__main__":
    main()
