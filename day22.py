from collections import defaultdict

import aoc


def _hash(s: int) -> int:
    """
    Calculate the result of multiplying the secret number by 64.
        Then, mix this result into the secret number.
        Finally, prune the secret number.
    Calculate the result of dividing the secret number by 32.
        Round the result down to the nearest integer.
        Then, mix this result into the secret number.
        Finally, prune the secret number.
    Calculate the result of multiplying the secret number by 2048.
        Then, mix this result into the secret number.
        Finally, prune the secret number.
    """
    s = mix(s, s * 64)
    s = prune(s)
    s = mix(s, s // 32)
    s = prune(s)
    s = mix(s, s * 2048)
    s = prune(s)
    return s


def mix(val: int, secret: int) -> int:
    """Mix the number using a bitwise XOR of the secret.
    if secret=42 and val=15 the result would be 37.
    """
    return val ^ secret


def prune(val: int) -> int:
    """Prune the number by using the modulo operator of 16777216.
    if secret=100_000_000 the output should be 16_113_920.
    """
    return val % 16_777_216


def calc1(s: int, rounds: int) -> int:
    for _ in range(rounds):
        s = _hash(s)
    return s


def calc2(s: int, rounds: int) -> dict[tuple[int, ...], int]:

    values: dict[tuple[int, ...], int] = {}
    keys: list[int] = []

    last = 0
    for idx in range(rounds):
        _last = int(str(s)[-1])
        if idx != 0:
            key = _last - last
            fs = tuple(keys[-4:])
            if fs not in values:
                values[fs] = last
            keys.append(key)
        last = _last

        s = _hash(s)
    return values


def part01(data: list[int]) -> int:
    t = 0
    for item in data:
        t += calc1(item, 2000)
    return t


def part02(val: list[int]) -> int:
    bests: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)

    for item in val:
        c = calc2(item, 2000)
        for k, v in c.items():
            if len(k) == 4:
                bests[k] += v

    return max(bests.values())


def run() -> None:
    # assert mix(15, 42) == 37
    # assert prune(100_000_000) == 16_113_920
    # assert calc(123, 10) == 5908254

    data = [a[0] for a in aoc.ints(r"./data/day22.txt")]
    assert part01(data) == 17577894908
    assert part02(data) == 1931


if __name__ == "__main__":
    run()
