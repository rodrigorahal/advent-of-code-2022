import copy
from collections import defaultdict


def simulate(stacks, instructions, multiple=False):
    for qty, from_idx, to_idx in instructions:

        from_stack = stacks[from_idx - 1]
        to_stack = stacks[to_idx - 1]

        elements = from_stack[-qty:]
        del from_stack[-qty:]

        if multiple:
            to_stack.extend(elements)
        else:
            to_stack.extend(reversed(elements))

    return stacks


def parse():
    stacks = []
    instructions = []
    stacks_by_idx = defaultdict(list)

    with open("05/input.txt") as f:
        blocks = f.read().split("\n\n")

        for line in blocks[0].split("\n"):
            i = 0
            idx = 0
            while i < len(line):
                if line[i] == " ":
                    i += 4
                    idx += 1
                elif line[i] == "[":
                    char = line[i + 1]
                    stacks_by_idx[idx].append(char)
                    i += 4
                    idx += 1

        for idx, stack in sorted(stacks_by_idx.items()):
            stacks.append(list(reversed(stack)))

        for line in blocks[1].split("\n"):
            contents = line.split()
            qty = int(contents[1])
            from_idx = int(contents[3])
            to_idx = int(contents[5])
            instructions.append((qty, from_idx, to_idx))

    return stacks, instructions


def main():
    stacks, instructions = parse()
    updated = simulate(copy.deepcopy(stacks), instructions)
    print(f"Part 1: {''.join([stack[-1] for stack in updated])}")

    updated = simulate(copy.deepcopy(stacks), instructions, multiple=True)
    print(f"Part 2: {''.join([stack[-1] for stack in updated])}")


if __name__ == "__main__":
    main()
