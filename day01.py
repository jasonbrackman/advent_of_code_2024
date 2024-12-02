from aoc import ints

def parse() -> tuple[list[int], list[int]]:
    r = ints(r'./data/day01.txt')
    l1 = []
    l2 = []
    for (a, b) in r:
        l1.append(a)
        l2.append(b)

    l1.sort()
    l2.sort()
    return l1, l2

def part01(l1: list[int], l2: list[int]) -> int:
    return sum(abs(a - b) for a, b in zip(l1, l2))

def part02(l1: list[int], l2: list[int]) -> int:
    return sum(
        sum([a == b for b in l2]) * a for a in l1
    )

def run():
    l1, l2 = parse()
    assert part01(l1, l2) == 1765812
    assert part02(l1, l2) == 20520794

if __name__ == "__main__":
    run()