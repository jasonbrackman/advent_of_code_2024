from collections import defaultdict

import aoc


def parse(path: str) -> defaultdict[str, set[str]]:
    results = defaultdict(set)
    for line in aoc.lines(path):
        a, b = line.split("-")
        results[a].add(b)
        results[b].add(a)
    return results


def part01(data) -> int:
    collection = set()
    for a, items in data.items():
        if not a.startswith("t"):
            continue
        for b in items:
            connections = [
                item for item in items if a in data[item] and b in data[item]
            ]
            for connection in connections:
                collection.add(frozenset((a, b, connection)))
    return len(collection)


def run() -> None:
    data = parse(r"./data/day23.txt")
    assert part01(data) == 1064


if __name__ == "__main__":
    run()
