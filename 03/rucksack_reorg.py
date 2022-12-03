import fileinput


def matching(rucksacks):
    priority = 0
    for rucksack in rucksacks:
        n = len(rucksack)
        fst, snd = rucksack[: n // 2], rucksack[n // 2 :]
        shared = next(iter(set(fst).intersection(set(snd))))
        priority += alpha_to_int(shared)
    return priority


def find(rucksacks):
    priority = 0
    for i in range(0, len(rucksacks), 3):
        a, b, c = rucksacks[i : i + 3]
        group = next(iter(set.intersection(set(a), set(b), set(c))))
        priority += alpha_to_int(group)
    return priority


def alpha_to_int(alpha):
    if alpha.islower():
        return ord(alpha) - ord("a") + 1
    return ord(alpha) - ord("A") + 27


def parse():
    return [line.strip() for line in fileinput.input()]


def main():
    rucksacks = parse()
    priority = matching(rucksacks)
    print(f"Part 1: {priority}")

    priority = find(rucksacks)
    print(f"Part 2: {priority}")


if __name__ == "__main__":
    main()
