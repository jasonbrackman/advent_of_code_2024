import aoc


def parse(path: str) -> tuple[list[str], list[str]]:
    lines = aoc.lines(path)
    parts = [a.strip() for a in next(lines).split(",")]
    goals = [l for l in lines if l]
    return parts, goals


def dfs(parts: list[str], goal: str, seen: dict[str, int]):
    if goal == "":
        return 1

    if goal in seen:
        return seen[goal]

    c = 0
    for f in parts:
        if goal.startswith(f):
            c += dfs(parts, goal[len(f) :], seen)

    seen[goal] = c
    return c


def part01(parts: list[str], goals: list[str]) -> int:
    return sum(dfs(parts, goal, {}) > 0 for goal in goals)


def part02(parts: list[str], goals: list[str]) -> int:
    return sum(dfs(parts, goal, {}) for goal in goals)


def run() -> None:
    path = r"./data/day19.txt"
    parts, goals = parse(path)
    assert part01(parts, goals) == 260
    assert part02(parts, goals) == 639963796864990


if __name__ == "__main__":
    run()
