from collections import defaultdict

import aoc


def parse(path):
    lines = aoc.lines(path)
    for line in lines:
        return [i for i in aoc.re_ints(line)]


def rules(val: int) -> list[int]:
    if val == 0:
        return [1]

    elif len(str(val)) % 2 == 0:
        s = str(val)
        return [int(s[: len(s) // 2]), int(s[len(s) // 2 :])]
    else:
        return [val * 2024]


def spin(c):
    n = defaultdict(int)
    for num, val in c.items():
        for item in rules(num):
            n[item] += val
    return n


def parts(data, spin_count) -> int:
    # breaking the rocks into subsequent pieces is not a problem, but the amount
    # of data drags the machine down.  Instead, track the numbers, carry them over
    # to the next iteration... and repeat.
    c: dict[int, int] = {d: 1 for d in data}
    for _ in range(spin_count):
        c = spin(c)
    return sum(c.values())


def run() -> None:
    path = r"./data/day11.txt"
    vals = parse(path)
    assert parts(vals, 25) == 197157
    assert parts(vals, 75) == 234430066982597


if __name__ == "__main__":
    run()
