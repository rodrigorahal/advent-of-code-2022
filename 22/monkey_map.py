import sys

CLOCK = [(0, 1), (1, 0), (0, -1), (-1, 0)]
COUNTER_CLOCK = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def walk(grid, path, start, dir=(0, 1), cube=False):
    row, col = start
    for cmd in path:
        if isinstance(cmd, int):
            row, col, dir = move(grid, (row, col), dir, cube=cube, steps=cmd)
        else:
            dir = turn(dir, to=cmd)
    return (row, col), dir


def move(grid, curr, dir, steps, cube=False):
    row, col = curr
    dr, dc = dir
    for _ in range(steps):
        if (row + dr, col + dc) in grid and grid[(row + dr, col + dc)] == ".":
            row, col = row + dr, col + dc
        elif (row + dr, col + dc) in grid and grid[(row + dr, col + dc)] == "#":
            break
        elif (row + dr, col + dc) not in grid:
            if cube:
                row, col, (dr, dc) = wrap_cube(grid, (row, col), (dr, dc))
            else:
                row, col = wrap(grid, (row, col), dir)
    return row, col, (dr, dc)


def wrap(grid, curr, dir):
    maxrow, maxcol = edges(grid)
    row, col = curr
    dr, dc = dir

    r, c = row, col

    if dr == 1:
        r = 0
    elif dr == -1:
        r = maxrow
    elif dc == -1:
        c = maxcol
    elif dc == 1:
        c = 0

    while (r, c) not in grid:
        r, c = r + dr, c + dc

    if grid[(r, c)] == ".":
        return r, c
    return row, col


def face(row, col):
    if 0 <= row < 50 and 50 <= col < 100:
        return 1
    elif 0 <= row < 50 and 100 <= col < 150:
        return 2
    elif 50 <= row < 100 and 50 <= col < 100:
        return 3
    elif 100 <= row < 150 and 50 <= col < 100:
        return 4
    elif 100 <= row < 150 and 0 <= col < 50:
        return 5
    elif 150 <= row < 200 and 0 <= col < 50:
        return 6
    assert False


def wrap_cube(grid, curr, dir):
    """
    From manually folding the input cube and working out mapping from faces

           ___________
          |  1  |  2  |
          |_____|_____|
          |  3  |
     _____|_____|
    |  5  |  4  |
    |_____|_____|
    |  6  |
    |_____|

    """
    row, col = curr
    dr, dc = dir
    face_ = face(row, col)

    if face_ == 1 and dr == -1:  # up
        drr, dcc = (0, 1)
        r = col + 100  # (50, 99) -> (150, 199)
        c = 0

    if face_ == 1 and dc == -1:  # left
        drr, dcc = (0, 1)
        r = 149 - row  # (0, 49) -> (149, 100)
        c = 0

    if face_ == 2 and dr == -1:  # up
        drr, dcc = (-1, 0)
        r = 199
        c = col - 100  # (100, 149) -> (0, 49)

    if face_ == 2 and dc == 1:  # right
        drr, dcc = (0, -1)
        r = 149 - row  # (0, 49) -> (149, 100)
        c = 99

    if face_ == 2 and dr == 1:  # down
        drr, dcc = (0, -1)
        r = col - 50  # (100, 149) -> (50, 99)
        c = 99

    if face_ == 3 and dc == 1:  # right
        drr, dcc = (-1, 0)
        r = 49
        c = row + 50  # (50, 99) -> (100, 149)

    if face_ == 3 and dc == -1:  # left
        drr, dcc = (1, 0)
        r = 100
        c = row - 50  # (50, 99) -> (0, 49)

    if face_ == 4 and dc == 1:  # right
        drr, dcc = (0, -1)
        r = 149 - row  # (100, 149) -> (49, 0)
        c = 149

    if face_ == 4 and dr == 1:  # down
        drr, dcc = (0, -1)
        c = 49
        r = col + 100  # (50, 99) -> (150, 199)

    if face_ == 5 and dr == -1:  # up
        drr, dcc = (0, 1)
        r = col + 50  # (0 , 49) -> (50, 99)
        c = 50

    if face_ == 5 and dc == -1:  # left
        drr, dcc = (0, 1)
        r = 149 - row  # (100, 149) -> (49, 0)
        c = 50

    if face_ == 6 and dc == 1:  # right
        drr, dcc = (-1, 0)
        r = 149
        c = row - 100  # (150, 199) -> (50, 99)

    if face_ == 6 and dr == 1:  # down
        drr, dcc = (1, 0)
        r = 0
        c = col + 100  # (0, 49) -> (100, 149)

    if face_ == 6 and dc == -1:  # left
        drr, dcc = (1, 0)
        r = 0
        c = row - 100  # (150, 199) -> (50, 99)

    assert (r, c) in grid
    if grid[(r, c)] == "#":
        return row, col, dir

    return r, c, (drr, dcc)


def turn(dir, to):
    if to == "R":
        idx = CLOCK.index(dir)
        return CLOCK[(idx + 1) % len(CLOCK)]
    elif to == "L":
        idx = COUNTER_CLOCK.index(dir)
        return COUNTER_CLOCK[(idx + 1) % len(COUNTER_CLOCK)]


def parse(filename):
    grid = {}
    path = []
    start = None
    with open(filename) as f:
        blocks = f.read().split("\n\n")

    for row, line in enumerate(blocks[0].split("\n")):
        for col, char in enumerate(line):
            if char in (".", "#"):
                grid[(row, col)] = char
                if not start:
                    start = (row, col)
    num = []
    for char in blocks[1]:
        if char.isdigit():
            num.append(char)
        else:
            path.append(int("".join(num)))
            num = []
            path.append(char)
    if num:
        path.append(int("".join(num)))
    return grid, path, start


def draw(grid):
    maxrow, maxcol = edges(grid)

    for row in range(maxrow + 1):
        line = [
            " " if (row, col) not in grid else grid[(row, col)]
            for col in range(maxcol + 1)
        ]
        print("".join(line))
    print()


def edges(grid):
    maxrow, maxcol = 0, 0
    for row, col in grid:
        maxrow = max(maxrow, row)
        maxcol = max(maxcol, col)
    return maxrow, maxcol


def password(row, col, dir):
    return 1000 * (row + 1) + 4 * (col + 1) + CLOCK.index(dir)


def main():
    grid, path, start = parse(sys.argv[1])
    (row, col), dir = walk(grid, path, start)
    print(f"Part 1: {password(row, col, dir)}")

    (row, col), dir = walk(grid, path, start, cube=True)
    print(f"Part 2: {password(row, col, dir)}")


if __name__ == "__main__":
    main()
