import aoc
from aoctypes import Vec2

W = 101
T = 103

Robots = dict[int, tuple[Vec2, Vec2]]


def parse(path) -> Robots:
    lines = aoc.lines(path)
    robots = [aoc.re_ints(line) for line in lines]

    r = {}
    for i, robot in enumerate(robots):
        px, py, vx, vy = robot
        r[i] = ((px, py), (vx, vy))
    return r


def add(p1: Vec2, p2: Vec2) -> Vec2:
    return (p1[0] + p2[0]) % W, (p1[1] + p2[1]) % T


def part01(robots: Robots) -> int:
    # simulate to 100
    for i in range(0, 100):
        for k, v in robots.items():
            p1, v1 = v
            robots[k] = add(p1, v1), v1

    # get quadrant values
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    for k, v in robots.items():
        (x, y), _ = v

        if x in (W // 2, W + 1 // 2) or y in (T // 2, T + 1 // 2):
            continue

        if x < W // 2:
            if y < T // 2:
                q1 += 1
            else:
                q2 += 1
        elif x > W // 2:
            if y < T // 2:
                q3 += 1
            else:
                q4 += 1

    return q1 * q2 * q3 * q4


def part02(robots: Robots) -> int:
    for i in range(1, 10_000):
        for k, v in robots.items():
            p1, v1 = v
            robots[k] = add(p1, v1), v1
        if is_tree(robots, i):
            return i


def is_tree(robots: Robots, count: int) -> bool:

    values = [k for (k, v) in robots.values()]
    # This worked -- but is slow.
    # graphic = 0
    # for j in range(T // 2):  # reduce scan
    #     for i in range(W // 3):  # reduce scan
    #         if (i, j) in values:
    #             graphic += 1
    #             if graphic == 6:  # is this an artistic line?
    #                 _display(values, count)
    #         else:
    #             graphic = 0

    # Not my idea -- but it is obviously hella fast.
    if len(values) == len(set(values)):
        # _display(values, count)
        return True
    return False


def _display(values: list[Vec2], count: int) -> None:
    print(f"ROUND: {count}")
    for j in range(T + 1):
        for i in range(W + 1):
            if (i, j) in values:
                print("#", end="")
            else:
                print(" ", end="")
        print()


def run() -> None:
    path = r"./data/day14.txt"

    robots = parse(path)
    assert part01(robots) == 218965032

    robots = parse(path)
    assert part02(robots) == 7037


if __name__ == "__main__":
    run()
