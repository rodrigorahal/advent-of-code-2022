import fileinput
from copy import deepcopy
from itertools import tee


SOURCE = (500, 0)


def simulate(grid):
    rest = 0
    maxx, maxy = edges(grid)
    while True:
        x, y = SOURCE
        while can_move(grid, x, y):
            x, y = move(grid, x, y)
            if y > maxy:
                return rest
        grid[(x, y)] = "o"
        rest += 1


def simulate_with_floor(grid):
    rest = 0
    maxx, maxy = edges(grid)
    floor_y = maxy + 2
    while True:
        x, y = SOURCE
        while can_move(grid, x, y, floor_y):
            x, y = move(grid, x, y, floor_y)
        grid[(x, y)] = "o"
        rest += 1
        if (x, y) == SOURCE:
            break
    return rest


def can_move(grid, x, y, floor_y=None):
    is_down_free = not in_grid(grid, x, y + 1, floor_y)
    is_down_left_free = not in_grid(grid, x - 1, y + 1, floor_y)
    is_down_right_free = not in_grid(grid, x + 1, y + 1, floor_y)

    return is_down_free or is_down_left_free or is_down_right_free


def in_grid(grid, x, y, floor_y=None):
    if not floor_y:
        return (x, y) in grid
    if y < floor_y:
        return (x, y) in grid
    return True


def move(grid, x, y, floor_y=None):
    is_down_free = not in_grid(grid, x, y + 1, floor_y)
    is_down_left_free = not in_grid(grid, x - 1, y + 1, floor_y)
    is_down_right_free = not in_grid(grid, x + 1, y + 1, floor_y)

    if is_down_free:
        return x, y + 1
    elif is_down_left_free:
        return x - 1, y + 1
    elif is_down_right_free:
        return x + 1, y + 1


def edges(grid):
    return max(x for x, y in grid), max(y for x, y in grid)


def parse():
    rocks = []
    for line in fileinput.input():
        edges = line.strip().split(" -> ")
        rocks.append([tuple(map(int, edge.split(","))) for edge in edges])
    return rocks


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def make_grid(rocks):
    grid = {}
    for rock in rocks:
        for (xa, ya), (xb, yb) in pairwise(rock):
            if xa == xb:
                for y in range(min(ya, yb), max(ya, yb) + 1):
                    grid[(xa, y)] = "#"
            elif ya == yb:
                for x in range(min(xa, xb), max(xa, xb) + 1):
                    grid[(x, ya)] = "#"
    return grid


def main():
    rocks = parse()
    grid = make_grid(rocks)
    rest = simulate(deepcopy(grid))
    print(f"Part 1: {rest}")
    rest = simulate_with_floor(deepcopy(grid))
    print(f"Part 2: {rest}")


if __name__ == "__main__":
    main()
