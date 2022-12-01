import fileinput


def top(calories, k=3):
    elf_cals = sorted([sum(elf) for elf in calories])
    return sum(elf_cals[-k:])


def count(calories):
    return max(sum(elf) for elf in calories)


def parse():
    calories = []
    elf = []

    file = fileinput.input()
    for line in file:
        if line == "\n":
            calories.append(elf)
            elf = []
            continue
        elf.append(int(line))
    calories.append(elf)

    return calories


def main():
    calories = parse()
    print(f"Part 1: {count(calories)}")
    print(f"Part 2: {top(calories)}")


if __name__ == "__main__":
    main()
