import fileinput
import math
from functools import cmp_to_key
from itertools import zip_longest

DIVIDERS = [[[2]], [[6]]]


def count(pairs):
    return sum(
        idx
        for idx, (left, right) in enumerate(pairs, start=1)
        if compare(left, right) == -1
    )


def reorder(pairs, dividers):
    packtes = []
    for left, right in pairs:
        packtes.append(left)
        packtes.append(right)
    for divider in dividers:
        packtes.append(divider)
    return sorted(packtes, key=cmp_to_key(compare))


def decoder_key(ordered, dividers):
    a, b = dividers
    return math.prod([ordered.index(a) + 1, ordered.index(b) + 1])


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        elif left < right:
            return -1
        else:
            return 1

    elif isinstance(left, list) and isinstance(right, list):
        for l, r in zip_longest(left, right, fillvalue=None):

            # left exhausted
            if l is None:
                return -1

            # right exhausted
            if r is None:
                return 1

            outcome = compare(l, r)
            if outcome != 0:
                return outcome
        return 0

    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)

    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])


def parse(filename):
    pairs = []
    with open(filename) as f:
        blocks = f.read().split("\n\n")
        for block in blocks:
            left, right = block.split("\n")
            pairs.append(tuple([eval(left), eval(right)]))
    return pairs


def main():
    pairs = parse("13/input.txt")
    print(f"Part 1: {count(pairs)}")
    ordered = reorder(pairs, DIVIDERS)
    print(f"Part 2: {decoder_key(ordered, DIVIDERS)}")


if __name__ == "__main__":
    main()
