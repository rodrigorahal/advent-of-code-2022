import fileinput


def count_contained(pairs):
    return sum(
        1 for (a, b) in pairs if is_fully_contained(a, b) or is_fully_contained(b, a)
    )


def count_overlaps(pairs):
    return sum(1 for (a, b) in pairs if has_overlap(a, b) or has_overlap(b, a))


def is_fully_contained(a, b):
    a_start, a_end = a
    b_start, b_end = b

    return b_start >= a_start and b_end <= a_end


def has_overlap(a, b):
    a_start, a_end = a
    b_start, b_end = b

    return a_start <= b_start <= a_end


def parse():
    pairs = []
    for line in fileinput.input():
        a, b = line.strip().split(",")
        a_start, a_end = tuple(map(int, a.split("-")))
        b_start, b_end = tuple(map(int, b.split("-")))
        pairs.append([(a_start, a_end), (b_start, b_end)])
    return pairs


def main():
    pairs = parse()
    count = count_contained(pairs)
    print(f"Part 1: {count}")

    count = count_overlaps(pairs)
    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
