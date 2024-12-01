import re

lut = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "t8t",
    "nine": "n9e",
}

def part01():
    x = 0
    with open(r'./data/day_01_2023.txt', encoding='utf-8') as f:
        for line in f:
            values = ''.join(re.findall(r'\d+', line))
            x += int(''.join([values[0], values[-1]]))
    assert x == 54708

def part02():
    x = 0
    with open(r'./data/day_01_2023.txt', encoding='utf-8') as f:
        for line in f:
            for item in lut:
                if item in line:
                    line = line.replace(item, lut[item])
            values = ''.join(re.findall(r'\d+', line))
            x += int(''.join([values[0], values[-1]]))
    assert x == 54087

part01()
part02()