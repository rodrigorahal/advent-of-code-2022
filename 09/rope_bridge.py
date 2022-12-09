import fileinput
import math

M = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}


def simulate(moves):
    H = (0, 0)
    T = (0, 0)
    positions = {(0, 0)}
    for dir, steps in moves:
        for step in range(steps):
            dr, dc = M[dir]
            hrow, hcol = H
            H = (hrow + dr, hcol + dc)
            T = move_tail(H, T)
            positions.add(T)
    return positions


def simulate_with_size(moves, size=10):
    knots = [(0, 0) for _ in range(size)]
    positions = {(0, 0)}
    for dir, steps in moves:
        for step in range(steps):
            dr, dc = M[dir]
            hr, hc = knots[0]
            knots[0] = (hr + dr, hc + dc)
            for i in range(1, size):
                knots[i] = move_tail(knots[i - 1], knots[i])
            positions.add(knots[-1])
    return positions


def move_tail(H, T):
    hrow, hcol = H
    trow, tcol = T

    if (hrow, hcol) in adjacent(trow, tcol):
        return T

    if hrow == trow:
        dc = int(math.copysign(1, hcol - tcol))
        return (trow, tcol + dc)

    if hcol == tcol:
        dr = int(math.copysign(1, hrow - trow))
        return (trow + dr, tcol)

    dr = int(math.copysign(1, hrow - trow))
    dc = int(math.copysign(1, hcol - tcol))

    return (trow + dr, tcol + dc)


def adjacent(row, col):
    adjacent = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            adjacent.append((row + dr, col + dc))
    return adjacent


def parse():
    return [
        (dir, int(steps))
        for dir, steps in [line.strip().split() for line in fileinput.input()]
    ]


def main():
    moves = parse()
    positions = simulate(moves)
    print(f"Part 1: {len(positions)}")
    positions = simulate_with_size(moves, size=10)
    print(f"Part 2: {len(positions)}")


if __name__ == "__main__":
    main()
