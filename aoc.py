from pathlib import Path
from typing import Iterator, Union
import re

NUM_PATTERN = re.compile(r'\d+')
WRD_PATTERN = re.compile(r'[a-zA-Z]+')

def lines(path: Union[Path, str]) -> Iterator[str]:
    with open(path, encoding='utf8') as handle:
        for line in handle:
            yield line.strip()

def ints(path: Union[Path, str]) -> Iterator[int]:
    for line in lines(path):
        yield re_ints(line)

def re_nums(s: str) -> list[str]:
    return re.findall(NUM_PATTERN, s)

def re_ints(s: str) -> list[int]:
    """Search for numbers in text and returns them as ints. If a number
    has consecutive digits beside each other they are considered one number:
    001 = [int(1)]
    2asdf2 = [int(2), int(2)]
    asdf45asdf = [int(45)]
    """
    return [int(ii) for ii in list(re_nums(s))]

def re_wrds(s: str) -> list[str]:
    """Search for clusters of uninterrupted text. Will ignore anything
    other than a-zA-Z."""
    return re.findall(WRD_PATTERN, s)
