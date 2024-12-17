class IntException(Exception):
    pass


class IntMachine:
    def __init__(self, r: dict[str, int], p: list[int]):
        self.r = r
        self.p = p
        self.pointer = 0
        self.buffer = []

    def _next(self):
        try:
            n = self.p[self.pointer]
        except IndexError as e:
            raise IntException

        self.pointer += 1
        return n

    def step(self):
        try:
            opcode = self._next()
            self.op(opcode)
        except IntException:
            return False
        # combo
        # print("Executing:", opcode, operand, self.r)

    def convert(self, val):
        if val in (0, 1, 2, 3):
            return val
        if val == 4:
            return self.r["A"]
        if val == 5:
            return self.r["B"]
        if val == 6:
            return self.r["C"]
        if val == 7:
            raise NotImplemented

    def op(self, arg1):

        if arg1 == 0:
            """
            The adv instruction (opcode 0) performs division. The numerator is the value
            in the A register. The denominator is found by raising 2 to the power of the
            instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2);
            an operand of 5 would divide A by 2^B.) The result of the division operation
            is truncated to an integer and then written to the A register.
            """
            arg2 = self.convert(self._next())
            val = int(self.r["A"] // 2**arg2)
            self.r["A"] = val

        elif arg1 == 1:
            """
            The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the
            instruction's literal operand, then stores the result in register B.
            """
            arg2 = self._next()  # literal operand
            self.r["B"] = self.r["B"] ^ arg2
        elif arg1 == 2:
            """The bst instruction (opcode 2) calculates the value of its combo operand
            modulo 8 (thereby keeping only its lowest 3 bits), then writes that value
            to the B register.
            """
            arg2 = self.convert(self._next())
            val = arg2 % 8
            self.r["B"] = val

        elif arg1 == 3:
            """The jnz instruction (opcode 3) does nothing if the A register is 0.
            However, if the A register is not zero, it jumps by setting the instruction
            pointer to the value of its literal operand; if this instruction jumps,
            the instruction pointer is not increased by 2 after this instruction.
            """
            if self.r["A"] != 0:
                arg2 = self._next()  # literal operand
                self.pointer = arg2

        elif arg1 == 4:
            """The bxc instruction (opcode 4) calculates the bitwise XOR of register
            B and register C, then stores the result in register B. (For legacy
            reasons, this instruction reads an operand but ignores it.)
            """
            _ = self._next()
            self.r["B"] = self.r["B"] ^ self.r["C"]

        elif arg1 == 5:
            """The out instruction (opcode 5) calculates the value of its combo
            operand modulo 8, then outputs that value. (If a program outputs
            multiple values, they are separated by commas.)
            """
            arg2 = self.convert(self._next())
            val = arg2 % 8
            self.buffer.append(val)

        elif arg1 == 6:
            """
            The bdv instruction (opcode 6) works exactly like the adv instruction
            except that the result is stored in the B register. (The numerator is
            still read from the A register.)
            """
            arg2 = self.convert(self._next())
            self.r["B"] = int(self.r["A"] / 2**arg2)
        elif arg1 == 7:
            """The cdv instruction (opcode 7) works exactly like the adv instruction
            except that the result is stored in the C register. (The numerator is
            still read from the A register.)"""
            arg2 = self.convert(self._next())
            self.r["C"] = int(self.r["A"] / 2**arg2)


def part01():
    m = IntMachine(  # no 707341301
        {"A": 25986278, "B": 0, "C": 0},
        [2, 4, 1, 4, 7, 5, 4, 1, 1, 4, 5, 5, 0, 3, 3, 0],
    )
    while True:
        r = m.step()
        if r is False:
            return ",".join([str(m) for m in m.buffer])
    raise ValueError


def part02():
    goal = [2, 4, 1, 4, 7, 5, 4, 1, 1, 4, 5, 5, 0, 3, 3, 0]
    for i in range(35_185_000_000_000, 38_100_000_001_000):
        m = IntMachine(
            {"A": i, "B": 0, "C": 0}, [2, 4, 1, 4, 7, 5, 4, 1, 1, 4, 5, 5, 0, 3, 3, 0]
        )
        while True:
            r = m.step()
            if r is False:
                print(m.buffer)
                print(i)
                if m.buffer == goal:
                    print("answer:", i)
                break


def tests():
    # m = IntMachine({"A": 0, "B": 0, "C": 9}, [2, 6])
    # while True:
    #     r = m.step()
    #     if not r:
    #         assert m.r["B"] == 1
    #         break
    #
    # m = IntMachine({"A": 10, "B": 0, "C": 0}, [5, 0, 5, 1, 5, 4])
    # while True:
    #     r = m.step()
    #     if r is False:
    #         break
    # print()
    # m = IntMachine({"A": 2024, "B": 0, "C": 0}, [0, 1, 5, 4, 3, 0])
    # while True:
    #     r = m.step()
    #     if r is False:
    #         break
    # print(m.r)
    #
    # m = IntMachine({"A": 0, "B": 29, "C": 0}, [1, 7])
    # while True:
    #     r = m.step()
    #     if r is False:
    #         break
    # print(m.r)
    #
    # m = IntMachine({"A": 0, "B": 2024, "C": 43690}, [4, 0])
    # while True:
    #     r = m.step()
    #     if r is False:
    #         break
    # print(m.r)
    # print("---" * 10)
    goal = [0, 3, 5, 4, 3, 0]
    for i in range(100_000_000):
        m = IntMachine({"A": i, "B": 0, "C": 0}, [0, 3, 5, 4, 3, 0])
        while True:
            r = m.step()
            if r is False:
                if m.buffer == goal:
                    print("Answer:", i)
                break
    """
    If register C contains 9, the program 2,6 would set register B to 1.
    If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    If register B contains 29, the program 1,7 would set register B to 26.
    If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354. 
    """


def run() -> None:
    # tests()
    assert part01() == "7,0,7,3,4,1,3,0,1"
    # part02()


if __name__ == "__main__":
    run()
