import fileinput


def count(cubes):
    faces = 0
    for cube in cubes:
        for neighbor in neighbors(*cube):
            if neighbor not in cubes:
                faces += 1
    return faces


def count_without_pockets(cubes):
    outside = search(cubes)
    faces = 0
    for cube in cubes:
        for neighbor in neighbors(*cube):
            if neighbor in outside:
                faces += 1
    return faces


def neighbors(x, y, z):
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }


def search(cubes, start=(-1, -1, -1)):
    maxx, maxy, maxz = edges(cubes)
    seen = set()
    stack = [(start)]

    while stack:
        curr = stack.pop()
        seen.add(curr)
        for neighbor in neighbors(*curr) - cubes - seen:
            nx, ny, nz = neighbor
            if -1 <= nx <= maxx + 1 and -1 <= ny <= maxy + 1 and -1 <= nz <= maxz + 1:
                stack.append(neighbor)
    return seen


def edges(cubes):
    maxx, maxy, maxz = 0, 0, 0
    for x, y, z in cubes:
        maxx = max(x, maxx)
        maxy = max(y, maxy)
        maxz = max(z, maxz)
    return maxx, maxy, maxz


def parse():
    return {tuple(map(int, line.strip().split(","))) for line in fileinput.input()}


def main():
    cubes = parse()
    print(f"Part 1: {count(cubes)}")
    print(f"Part 2: {count_without_pockets(cubes)}")


if __name__ == "__main__":
    main()
