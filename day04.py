import aoc

PATH = r"data/day04.txt"
SEARCH = ("XMAS", "SAMX")


def part01():
    t = 0
    rows = list(aoc.lines(PATH))

    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c in "XS":
                # check forward
                if row[i : i + 4] in SEARCH:
                    t += 1

                # check down
                if len(rows) > j + 3:
                    stack = (
                        rows[j][i] + rows[j + 1][i] + rows[j + 2][i] + rows[j + 3][i]
                    )
                    if stack in SEARCH:
                        t += 1

                # check diagonal
                if len(row) > j + 3:
                    # diagonal to the right
                    if len(rows) > i + 3:
                        diagr = (
                            rows[j][i]
                            + rows[j + 1][i + 1]
                            + rows[j + 2][i + 2]
                            + rows[j + 3][i + 3]
                        )
                        if diagr in SEARCH:
                            t += 1

                    # diagonal to the left
                    if i - 3 >= 0:
                        diagl = (
                            rows[j][i]
                            + rows[j + 1][i - 1]
                            + rows[j + 2][i - 2]
                            + rows[j + 3][i - 3]
                        )
                        if diagl in SEARCH:
                            t += 1
    assert t == 2414


def part02():
    t = 0
    lines = list(aoc.lines(PATH))

    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            if c in "A":
                if (
                    # Ensure a check won't fall off the board
                    j - 1 >= 0
                    and j + 1 < len(lines)
                    and i - 1 >= 0
                    and i + 1 < len(line)
                ):
                    # ensure corners make sense
                    counts = {"M": 0, "S": 0}

                    c1 = lines[j - 1][i - 1]
                    c2 = lines[j - 1][i + 1]
                    c3 = lines[j + 1][i - 1]
                    c4 = lines[j + 1][i + 1]
                    if c1 != c4 and c2 != c3:
                        for item in (c1, c2, c3, c4):
                            if item not in counts:
                                continue
                            counts[item] += 1
                        if counts["M"] == 2 and counts["S"] == 2:
                            t += 1

    assert t == 1871


def run() -> None:
    part01()
    part02()


if __name__ == "__main__":
    run()
