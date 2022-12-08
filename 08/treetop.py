import fileinput
import math


def count(grid):
    visible = 0
    for row, heights in enumerate(grid):
        for col, height in enumerate(heights):
            if is_visible(grid, row, col):
                visible += 1
    return visible


def find(grid):
    score = 0
    for row, heights in enumerate(grid):
        for col, height in enumerate(heights):
            score = max(score, scenic_score(grid, row, col))
    return score


def scenic_score(grid, row, col):
    scores = []
    height = grid[row][col]
    H, W = len(grid), len(grid[0])
    for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        visible = 0
        r, c = row + dr, col + dc
        while 0 <= r < H and 0 <= c < W:
            if grid[r][c] >= height:
                visible += 1
                break
            visible += 1
            r, c = (r + dr, c + dc)
        scores.append(visible)
    return math.prod(scores)


def is_visible(grid, row, col):
    height = grid[row][col]
    n = len(grid)

    if row in (0, n - 1) or col in (0, n - 1):
        return True

    left = all(h < height for h in grid[row][:col])
    right = all(h < height for h in grid[row][col + 1 :])
    up = all(h < height for h in [grid[r][col] for r in range(0, row)])
    down = all(h < height for h in [grid[r][col] for r in range(row + 1, n)])

    return any([left, right, up, down])


def parse():
    grid = []
    for line in fileinput.input():
        row = line.strip()
        grid.append([int(char) for char in row])
    return grid


def main():
    grid = parse()
    print(f"Part 1: {count(grid)}")
    print(f"Part 2: {find(grid)}")


if __name__ == "__main__":
    main()
