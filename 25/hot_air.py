import fileinput
from typing import List

S_TO_D = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
D_TO_S = {0: "=", 1: "-", 2: "0", 3: "1", 4: "2"}


def from_snafu(num: str):
    return sum(pow(5, p) * S_TO_D[d] for p, d in enumerate(reversed(num)))


def to_snafu(num: int) -> str:
    snafu = []
    quo, res = divmod(num + 2, 5)
    snafu.append(D_TO_S[res])
    while quo:
        quo, res = divmod(quo + 2, 5)
        snafu.append(D_TO_S[res])
    return "".join(reversed(snafu))


def parse():
    return [line.strip() for line in fileinput.input()]


def main():
    nums = parse()
    print(f"Part 1: {to_snafu(sum(from_snafu(num) for num in nums))}")


if __name__ == "__main__":
    main()
