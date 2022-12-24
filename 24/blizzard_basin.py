import fileinput
from copy import deepcopy
from collections import deque


DIRS = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


def search(grid, blizzard, start, targets):
    grid_by_t = {0: grid}
    blizzard_by_t = {0: blizzard}
    queue = deque([(start, 0)])
    seen = set()

    while queue:
        curr, t = queue.popleft()
        row, col = curr

        if curr == targets[-1]:
            targets.pop()
            if not targets:
                return t
            queue.clear()
            queue.append([(row, col), t])
            continue

        if (curr, t) in seen:
            continue

        seen.add((curr, t))

        if t + 1 not in grid_by_t:
            updated_grid, updated_blizzard = evolve(grid_by_t[t], blizzard_by_t[t])
            grid_by_t[t + 1] = updated_grid
            blizzard_by_t[t + 1] = updated_blizzard

        for nrow, ncol in neighbors(grid, row, col):
            if grid_by_t[t + 1][nrow][ncol] == ".":
                queue.append([(nrow, ncol), t + 1])
    return -1


def evolve(grid, blizzard):
    H, W = len(grid), len(grid[0])
    updated_blizzard = set()
    occupied = set()
    updated_grid = deepcopy(grid)

    for row, col, dir in blizzard:
        dr, dc = DIRS[dir]
        if dc and col + dc == W - 1:
            col = 0
        elif dc and col + dc == 0:
            col = W - 1
        elif dr and row + dr == H - 1:
            row = 0
        elif dr and row + dr == 0:
            row = H - 1

        updated_blizzard.add((row + dr, col + dc, dir))
        occupied.add((row + dr, col + dc))

    for row, cols in enumerate(updated_grid):
        for col, pos in enumerate(cols):
            if pos == "#":
                continue
            if (row, col) in occupied:
                updated_grid[row][col] = "b"
            else:
                updated_grid[row][col] = "."

    return updated_grid, updated_blizzard


def neighbors(grid, row, col):
    H, W = len(grid), len(grid[0])
    res = []
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
        if 0 <= (row + dr) < H and 0 <= (col + dc) < W:
            res.append((row + dr, col + dc))
    return res


def parse():
    grid = []
    blizzard = set()
    for r, line in enumerate(fileinput.input()):
        row = []
        for c, char in enumerate(line.strip()):
            if char in "<>v^":
                blizzard.add((r, c, char))
            row.append(char)
        grid.append(row)
    return grid, blizzard


def draw(grid):
    for row in grid:
        print("".join(row))
    print()


def main():
    grid, blizzard = parse()
    H, W = len(grid), len(grid[0])
    time = search(grid, blizzard, start=(0, 1), targets=[(H - 1, W - 2)])
    print(f"Part 1: {time}")

    time = search(
        grid, blizzard, start=(0, 1), targets=[(H - 1, W - 2), (0, 1), (H - 1, W - 2)]
    )
    print(f"Part 2: {time}")


if __name__ == "__main__":
    main()
