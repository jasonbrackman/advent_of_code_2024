import aoc
from aoc import AOCException, Grid, Vec2


dirs = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}

turn = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def part01(data: Grid) -> set[Vec2]:
    y, x = find_start(data)
    dir_ = dirs[data[y][x]]
    data[y][x] = "."

    visited = set()
    q = {(y, x)}

    while q:
        y, x = q.pop()

        # get new pos
        b, a = y + dir_[0], x + dir_[1]

        # if on grid...
        if 0 <= b < len(data) and 0 <= a < len(data[0]):
            if data[b][a] == ".":
                visited.add((b, a))
                q.add((b, a))
            else:
                # blocked so turn and requeue based on new direction...
                dir_ = turn[dir_]
                q.add((y, x))

    return visited


def part02(data: Grid, visited: set[Vec2]) -> int:
    t = 0
    y, x = find_start(data)
    dir_ = dirs[data[y][x]]
    data[y][x] = "."
    for yy, xx in visited:
        if (yy, xx) != (y, x):
            # create blocker on path.
            data[yy][xx] = "#"

            t += is_looped(data, dir_, (y, x))

            # reset blocker
            data[yy][xx] = "."

    return t


def find_start(data: Grid) -> Vec2:
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] in "^v><":
                return y, x
    raise AOCException("No Starting Point Found.")


def is_looped(data: Grid, dir_: Vec2, start_pos: Vec2) -> bool:
    visited = set()
    q = {start_pos}
    while q:
        y, x = q.pop()
        b, a = y + dir_[0], x + dir_[1]
        if ((b, a), dir_) in visited:
            return True

        if 0 <= b < len(data) and 0 <= a < len(data[0]):
            if data[b][a] == ".":
                visited.add(((b, a), dir_))
                q.add((b, a))
            else:
                dir_ = turn[dir_]
                q.add((y, x))
    return False


def run() -> None:
    path = r"./data/day06.txt"
    data = aoc.grid(path)
    visited = part01(data)
    assert len(visited) == 5131

    data = aoc.grid(path)
    assert part02(data, visited) == 1784


if __name__ == "__main__":
    run()
