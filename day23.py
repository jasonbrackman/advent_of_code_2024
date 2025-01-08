from collections import defaultdict

import aoc


def parse(path: str) -> defaultdict[str, set[str]]:
    results = defaultdict(set)
    for line in aoc.lines(path):
        a, b = line.split("-")
        results[a].add(b)
        results[b].add(a)
    return results


def in_set(a, b, items, data):
    r = [item for item in items if a in data[item] and b in data[item]]
    return r


def part01(data) -> int:
    collection = set()
    for k, v in data.items():
        if not k.startswith("t"):
            continue
        for item in v:
            connections = in_set(k, item, v, data)
            for connection in connections:
                collection.add(frozenset((k, item, connection)))
    return len(collection)


def run() -> None:
    data = parse(r"./data/day23.txt")
    assert part01(data) == 1064


if __name__ == "__main__":
    run()
