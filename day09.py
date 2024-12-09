import aoc
from collections import deque


def parse(path: str) -> deque[int]:
    results = aoc.lines(path)
    return deque([int(s) for s in next(results)])


def part01(data: deque[int]) -> int:
    contiguous, _ = get_mem_blocks(data)

    i = 0
    # then push things to the right 'spaces'
    while contiguous and i < len(contiguous):
        if contiguous[i] == ".":
            p = contiguous.pop()
            while p == ".":
                p = contiguous.pop()
            contiguous[i] = p
        i += 1

    # then get final checksum
    checksum = sum(i * j for i, j in enumerate(contiguous))
    return checksum


def part02(data: deque[int]) -> int:
    _, blocks = get_mem_blocks(data)
    for idx1 in range(len(blocks) - 1, -1, -1):
        c1, t1 = blocks[idx1]
        if "." not in set(t1):
            # found something to find a memory slot
            for idx, (c2, t2) in enumerate(blocks):
                # Ensure that we don't pass the block needing to be pushed left
                # Note: this was a bug that caused a lot of pain
                if idx == idx1:
                    break

                if c2 >= len(t1):
                    original_length = len(blocks[idx][1])
                    blocks[idx][0] -= len(t1)
                    blocks[idx][1] = (
                        [v for v in t2 if v != "."] + t1 + (["."] * blocks[idx][0])
                    )
                    assert original_length == len(blocks[idx][1])
                    blocks[idx1][1] = ["." for _ in t1]
                    break
    items = []
    for count, space in blocks:
        items.extend(space)

    checksum = sum(i * j for i, j in enumerate(items) if j != ".")
    return checksum


def get_mem_blocks(data: deque[int]):
    blocks = []
    contiguous = []
    id_ = 0
    switch = True

    while data:
        val = data.popleft()
        if switch:
            contiguous.extend([id_] * val)
            blocks.append([0, [id_] * val])
            id_ += 1
        else:
            if val > 0:
                blocks.append([val, ["."] * val])
            contiguous.extend(["."] * val)
        switch = not switch
    return contiguous, blocks


def run() -> None:
    path = r"./data/day09.txt"
    data = parse(path)
    assert part01(deque(data)) == 6334655979668
    assert part02(data) == 6349492251099


if __name__ == "__main__":
    run()
