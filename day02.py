import aoc

PATH_ = r"./data/day02t.txt"
PATH = r"./data/day02.txt"

Reports = list[list[int]]
Levels = list[int]


def parse() -> Reports:
    # need to reuse so return as a list (only 1k lines)
    return list(aoc.ints(PATH))


def _is_safe(levels: Levels) -> bool:

    safe = True
    c = None

    # check to see if all are ordered
    xx = list(sorted(levels))
    xy = list(reversed(xx))
    if levels not in (xx, xy):
        safe = False
    else:
        for level in levels:
            if c is None:
                c = level
            else:
                # Rule says must be a diff of 1-3 between each level
                if 1 <= abs(level - c) <= 3:
                    c = level
                else:
                    safe = False
                    break
    return safe


def part01(reports: Reports) -> int:
    return sum(_is_safe(levels) for levels in reports)


def part02(reports: Reports) -> int:
    count = 0

    for levels in reports:
        index = 0
        safe = _is_safe(levels)
        while index < len(levels) and safe is False:
            new_level = list(levels)
            del new_level[index]
            safe = _is_safe(new_level)
            index += 1

        count += int(safe)

    return count


def run() -> None:
    reports = parse()
    assert part01(reports) == 510
    assert part02(reports) == 553


if __name__ == "__main__":
    run()
