from typing import Iterator

import aoc

Update = list[int]


class Manual:
    def __init__(self):
        self._rules: set[tuple[int, ...]] = set()
        self._updates: list[Update] = []

    @property
    def rules(self) -> Iterator[tuple[int, ...]]:
        return iter(self._rules)

    @property
    def updates(self) -> Iterator[Update]:
        return iter(self._updates)

    def add_rule(self, s: str) -> None:
        self._rules.add(tuple(aoc.re_ints(s)))

    def add_update(self, s: str) -> None:
        self._updates.append(list(aoc.re_ints(s)))

    def validate(self, update: Update) -> bool:
        for a, b in self.rules:
            if a in update and b in update:
                if update.index(a) < update.index(b):
                    continue
                return False
        return True


def parse(path: str) -> Manual:
    manual = Manual()
    lines = aoc.lines(path)
    rules = True
    for line in lines:
        if line == "":
            rules = False
        elif rules:
            manual.add_rule(line)
        else:
            manual.add_update(line)
    return manual


def part01(m: Manual) -> None:
    t = 0
    for update in m.updates:
        if m.validate(update):
            t += update[len(update) // 2]
    assert t == 4766


def part02(m):
    t = 0
    for update in m.updates:
        if good := m.validate(update):
            continue

        while good is False:
            good = True
            for a, b in m.rules:
                if a in update and b in update:
                    if update.index(a) > update.index(b):
                        good = False
                        x = update.index(a)
                        y = update.index(b)
                        update[x], update[y] = update[y], update[x]

        t += update[len(update) // 2]
    assert t == 6257


def run() -> None:
    path = r"./data/day05.txt"
    manual = parse(path)
    part01(manual)
    part02(manual)


if __name__ == "__main__":
    run()
