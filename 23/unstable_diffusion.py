import fileinput
from collections import defaultdict, deque
from copy import deepcopy


CARDS = ["N", "NE", "NW", "S", "SE", "SW", "E", "W"]
DIRS = [["N", "NE", "NW"], ["S", "SE", "SW"], ["W", "NW", "SW"], ["E", "NE", "SE"]]


def count(grid):
    minrow, maxrow, mincol, maxcol = edges(grid)
    return sum(
        grid[(row, col)] == "."
        for row in range(minrow, maxrow + 1)
        for col in range(mincol, maxcol + 1)
    )


def run(grid, dirs, rounds=10):
    for r in range(1, rounds):
        moved = round(grid, dirs)
        if not moved:
            break
        dirs.rotate(-1)
    return grid, r


def round(grid, dirs):
    proposed = defaultdict(list)
    moved = 0

    elfs = [(row, col) for (row, col) in grid if grid[(row, col)] == "#"]

    for (row, col) in elfs:
        neighbor_by_dir = neighbors(grid, row, col)

        if not any(grid[neighbor_by_dir[dir]] == "#" for dir in CARDS):
            continue

        for A, B, C in dirs:
            if not any(grid[neighbor_by_dir[dir]] == "#" for dir in [A, B, C]):
                proposed[neighbor_by_dir[A]].append((row, col))
                break

    for (row, col), by in proposed.items():
        if len(by) == 1:
            [(orow, ocol)] = by
            grid[(row, col)] = "#"
            del grid[(orow, ocol)]
            moved += 1
    return moved


def neighbors(grid, row, col):
    coords = []
    for dr in [-1, 1, 0]:
        for dc in [0, 1, -1]:
            if dr == 0 and dc == 0:
                continue
            coords.append((row + dr, col + dc))
    return dict(zip(CARDS, coords))


def parse():
    grid = defaultdict(lambda: ".")
    for row, line in enumerate(fileinput.input()):
        for col, char in enumerate(line.strip()):
            grid[(row, col)] = char
    return grid


def draw(grid):
    minrow, maxrow, mincol, maxcol = edges(grid)

    for row in range(minrow, maxrow + 1):
        line = [
            grid[(row, col)] if (row, col) in grid else "."
            for col in range(mincol, maxcol + 1)
        ]
        print("".join(line))
    print()


def edges(grid):
    minrow = maxrow = mincol = maxcol = 0
    for row, col in grid:
        if grid[(row, col)] != "#":
            continue
        minrow = min(minrow, row)
        maxrow = max(maxrow, row)
        mincol = min(mincol, col)
        maxcol = max(maxcol, col)
    return minrow, maxrow, mincol, maxcol


def main():
    grid = parse()
    state, _ = run(deepcopy(grid), deque(DIRS), rounds=10)
    print(f"Part 1: {count(state)}")

    _, r = run(deepcopy(grid), deque(DIRS), rounds=10000)
    print(f"Part 2: {r}")


if __name__ == "__main__":
    main()
