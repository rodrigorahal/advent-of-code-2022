import fileinput
from collections import deque


def search(grid, S, E):
    queue = deque([(s, 0) for s in S])
    seen = set()

    while queue:
        (row, col), steps = queue.popleft()
        if (row, col) in seen:
            continue
        if (row, col) == E:
            return steps
        seen.add((row, col))

        for nr, nc in neighbors(grid, row, col):
            if ord(grid[nr][nc]) - ord(grid[row][col]) <= 1:
                queue.append(((nr, nc), steps + 1))
    return None


def candidates(grid):
    S = []
    for row, heights in enumerate(grid):
        for col, height in enumerate(heights):
            if height == "a":
                S.append((row, col))
    return S


def neighbors(grid, row, col):
    H, W = len(grid), len(grid[0])
    return [
        (row + dr, col + dc)
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= row + dr < H and 0 <= col + dc < W
    ]


def parse():
    grid = []
    S, E = None, None
    grid = [[char for char in line.strip()] for line in fileinput.input()]
    for row, heights in enumerate(grid):
        for col, height in enumerate(heights):
            if height == "S":
                grid[row][col] = "a"
                S = (row, col)
            elif height == "E":
                grid[row][col] = "z"
                E = (row, col)
    return grid, S, E


def main():
    grid, S, E = parse()
    steps = search(grid, [S], E)
    print(f"Part 1: {steps}")
    steps = search(grid, candidates(grid), E)
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    main()
