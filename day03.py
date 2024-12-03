import aoc
import math
import re

PATH = r"./data/day03.txt"

pattern = re.compile("mul\(\d+,\d+\)")


def _mult(line) -> int:
    t = 0
    results = pattern.findall(line)
    for result in results:
        nums = aoc.re_ints(result)
        t += math.prod(nums)
    return t


def part01(line: str) -> int:
    return _mult(line)


def part02(line: str) -> int:
    t = 0

    # every part starts in the enabled position
    parts = line.split("do()")

    for part in parts:
        # every part _may_ contain a disabler
        dont = part.index("don't()") if "don't()" in part else -1
        part = part[:dont]
        t += _mult(part)
    return t


def run() -> None:
    data = aoc.lines(PATH)
    line = "".join(data)
    assert part01(line) == 183380722
    assert part02(line) == 82733683


if __name__ == "__main__":
    run()
