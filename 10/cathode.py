import fileinput
from collections import deque

CYCLES = {20, 60, 100, 140, 180, 220}


def run(tape, cycles=221):
    reg = 1
    in_progress = None
    score = 0
    for cycle in range(1, cycles):
        if cycle in CYCLES:
            score += cycle * reg
        reg, in_progress = step(reg, in_progress, tape)
    return score


def step(reg, in_progress, tape):
    if in_progress:
        cmd, qty = in_progress
        return reg + qty, None

    cmd = tape.popleft()
    if cmd[0] == "addx":
        return reg, cmd

    return reg, in_progress


def run_with_screen(tape, cycles=241, width=40):
    reg = 1
    in_progress = None
    screen = []
    for cycle in range(1, cycles):
        pixel = cycle % width - 1 if cycle % width else width - 1
        screen.append("#" if pixel in (reg - 1, reg, reg + 1) else " ")
        reg, in_progress = step(reg, in_progress, tape)
    return screen


def draw(screen, width=40):
    for i in range(0, len(screen), width):
        print("".join(screen[i : i + width]))


def parse():
    tape = []
    for line in fileinput.input():
        contents = line.strip().split()
        if len(contents) == 1:
            tape.append(tuple(contents))
        else:
            tape.append((contents[0], int(contents[1])))
    return tape


def main():
    tape = parse()
    score = run(deque(tape))
    print(f"Part 1: {score}")
    screen = run_with_screen(deque(tape))
    print("Part 2:")
    print(f"{draw(screen)}")


if __name__ == "__main__":
    main()
