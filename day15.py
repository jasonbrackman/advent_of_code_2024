from typing import Optional

import aoc
from dataclasses import dataclass, field

from aoctypes import Vec2

Block = list[Vec2]
Grid = list[list[str]]
DIRS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


@dataclass
class Space:
    pos: Block
    val: list[str]

    # need original positions to clear first before moving, this allows the next
    # set to populate the cleared area and so on .. till we are at the start of the
    # chain.
    ori: Optional[Block] = field(default=list)

    def move(self, d: Vec2) -> None:
        self.ori = list(self.pos)
        self.pos = [(y + d[0], x + d[1]) for y, x in self.pos]

    @staticmethod
    def full_block(p1, val):
        """Some additional logic needed here to find out if the position is a
        wide block containing two positions."""
        other = []
        if val == "[":
            other.append(p1)
            other.append((p1[0] + DIRS[">"][0], p1[1] + DIRS[">"][1]))
        elif val == "]":
            other.append((p1[0] + DIRS["<"][0], p1[1] + DIRS["<"][1]))
            other.append(p1)
        return other

    def bump(self, p1: Vec2, grid: Grid) -> Block:
        """Find out what blocks will be bumped if things move.Use this to process
        down the chain until there is a block."""
        bumped = []
        for y, x in self.pos:
            yy = y + p1[0]
            xx = x + p1[1]
            if (yy, xx) not in self.pos:
                full = self.full_block((yy, xx), grid[yy][xx])
                bumped.extend(full)
        return bumped

    def peek(self, d: Vec2, grid: Grid) -> bool:
        """can the blocks move to the next position?"""
        for y, x in self.pos:
            yy = y + d[0]
            xx = x + d[1]
            if "#" == grid[yy][xx]:
                return False
        return True


@dataclass
class GridBase:
    _grid: Grid
    _inst: list[str]

    @classmethod
    def load(cls, path: str) -> "GridBase":
        raise NotImplemented

    def sim(self) -> None:
        raise NotImplemented

    def total(self, key: str) -> int:
        return self._total(key)

    def display(self):
        for j in range(len(self._grid)):
            for i in range(len(self._grid[0])):
                print(self._grid[j][i], end="")
            print()

    def get_start_pos(self) -> Vec2:
        for j in range(len(self._grid)):
            for i in range(len(self._grid[0])):
                if self._grid[j][i] == "@":
                    return j, i

    def get_value(self, p1) -> str:
        j, i = p1
        return self._grid[j][i]

    def add(self, p1: Vec2, p2: Vec2) -> Vec2:
        return p1[0] + p2[0], p1[1] + p2[1]

    def _total(self, key) -> int:
        t = 0
        for j in range(len(self._grid)):
            for i in range(len(self._grid[0])):
                if self.get_value((j, i)) == key:
                    t += 100 * j + i
        return t


@dataclass
class M(GridBase):

    @classmethod
    def load(cls, path: str) -> "M":
        grid = []
        inst = []
        lines = aoc.lines(path)
        get_grid = True
        for line in lines:

            if not line:
                get_grid = False
            if get_grid:
                grid.append(list(line))
            else:
                inst.extend(list(line))

        return M(grid, inst)

    def sim(self):
        # DIRS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
        start = self.get_start_pos()
        for inst in self._inst:
            # print("Moving:", inst)
            d = DIRS[inst]
            new_pos = self.add(start, d)

            val = self.get_value(new_pos)
            if val == ".":
                self.move(start, new_pos)
                start = new_pos
            elif val == "#":
                continue
            elif val == "O":
                stack = [start, new_pos]
                startp = new_pos
                should_move = False
                while True:
                    # find out if there is any space to move
                    t = self.add(new_pos, d)
                    v = self.get_value(t)
                    if v == "#":
                        # start stays where it is
                        break
                    elif v == ".":
                        stack.append(t)
                        should_move = True
                        start = startp
                        break

                    elif v == "O":
                        # print("yes!")
                        stack.append(t)
                        new_pos = t

                if should_move:
                    # this is related for narrow loads
                    for index in range(len(stack) - 1, 0, -1):
                        # print(index, stack[index], stack[index - 1])
                        j, i = stack[index]
                        jj, ii = stack[index - 1]
                        self._grid[j][i], self._grid[jj][ii] = (
                            self._grid[jj][ii],
                            self._grid[j][i],
                        )
            # self.display()

    def move(self, p1: Vec2, p2: Vec2) -> None:
        j, i = p1
        jj, ii = p2
        self._grid[j][i], self._grid[jj][ii] = self._grid[jj][ii], self._grid[j][i]


@dataclass
class W(GridBase):

    @classmethod
    def load(cls, path: str) -> GridBase:
        grid = []
        inst = []
        lines = aoc.lines(path)
        get_grid = True
        for line in lines:

            if not line:
                get_grid = False
            if get_grid:
                n = []
                for a, b in zip(line, line):
                    if a == "#":
                        n += [a, b]
                    elif a == ".":
                        n += [a, b]
                    elif a == "O":
                        n += ["[", "]"]
                    elif a == "@":
                        n += [a, "."]
                grid.append(list(n))
            else:
                inst.extend(list(line))

        return W(grid, inst)

    def sim(self):
        for inst in self._inst:
            start_pos = self.get_start_pos()
            space = Space([start_pos], ["@"])
            work = []
            d = DIRS[inst]
            q = [space]
            while q:
                s = q.pop()
                if s.peek(d, self._grid):
                    new = s.bump(d, self._grid)
                    if new:
                        q.append(Space(new, [self.get_value(p1) for p1 in new]))
                    s.move(d)
                    work.append(s)
                else:
                    work.clear()
            if work:

                for w in work:
                    for yy, xx in w.ori:
                        self._grid[yy][xx] = "."
                for w in work:
                    for (y, x), v in zip(w.pos, w.val):
                        self._grid[y][x] = v

    def get_full_space(self, p1: Vec2, val: str) -> Vec2:
        other = []
        if val == "[":
            other.append(p1)
            other.append(self.add(p1, DIRS[">"]))
        else:
            other.append(self.add(p1, DIRS["<"]))
            other.append(p1)
        return other


def part01(path: str) -> int:
    m = M.load(path)
    m.sim()
    return m.total("O")


def part02(path) -> int:
    m = W.load(path)
    m.sim()
    return m.total("[")


def run() -> None:
    path = r"./data/day15.txt"
    assert part01(path) == 1505963

    path = r"./data/day15.txt"
    assert part02(path) == 1543141


if __name__ == "__main__":
    run()
