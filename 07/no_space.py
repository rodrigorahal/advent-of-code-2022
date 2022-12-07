import fileinput
from collections import defaultdict


def sizes(output):
    size_by_name = defaultdict(int)
    cwd = None
    stack = []

    for line in output:
        if line[1] == "cd":
            if line[2] == "..":
                path = "/".join(stack)
                size_by_name[path] += size_by_name[f"{path}/{cwd}"]
                cwd = stack.pop()
            elif line[2] == "/":
                cwd = line[2]
            else:
                stack.append(cwd)
                cwd = line[2]
        elif line[1] == "ls":
            continue
        elif line[0] == "dir":
            continue
        else:
            size = int(line[0])
            size_by_name["/".join(stack + [cwd])] += size

    while stack:
        path = "/".join(stack)
        size_by_name[path] += size_by_name[f"{path}/{cwd}"]
        cwd = stack.pop()
    return size_by_name


def find(size_by_name, treshold=100_000):
    return [(dir, size) for dir, size in size_by_name.items() if size <= treshold]


def delete(size_by_name, total_size=70_000_000, required_size=30_000_000):
    curr_used = size_by_name["/"]
    curr_unused = total_size - curr_used
    min_delete_size = required_size - curr_unused
    candidate = min(size for size in size_by_name.values() if size >= min_delete_size)
    return candidate


def parse():
    return [line.strip().split() for line in fileinput.input()]


def main():
    output = parse()
    size_by_name = sizes(output)
    dirs = find(size_by_name)
    print(f"Part 1: {sum(size for _,size in dirs)}")

    print(f"Part 2: {delete(size_by_name)}")


if __name__ == "__main__":
    main()
