import math
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from typing import Deque, Dict, List


@dataclass
class Monkey:
    id: int
    items: Deque[int]
    operation: List[str]
    divisible_by: int
    if_true: int
    if_false: int


def simulate(monkeys: Dict[int, Monkey], rounds: int = 20, with_ease: bool = True):
    inspected_by_monkey = defaultdict(int)
    for _ in range(rounds):
        round(monkeys, inspected_by_monkey, with_ease)
    return inspected_by_monkey


def monkey_biz(inspected_by_monkey: Dict[int, int]):
    return math.prod(sorted(inspected_by_monkey.values())[-2:])


def prime_lcm(monkeys: Dict[int, Monkey]):
    return math.prod(monkey.divisible_by for monkey in monkeys.values())


def round(
    monkeys: Dict[int, Monkey], inspected_by_monkey: Dict[int, int], with_ease: bool
):
    for i in range(len(monkeys)):
        monkey = monkeys[i]
        while monkey.items:
            level = monkey.items.popleft()
            level = operate(monkey.operation, level)
            if with_ease:
                level //= 3
            else:
                level %= prime_lcm(monkeys)
            if level % monkey.divisible_by == 0:
                monkeys[monkey.if_true].items.append(level)
            else:
                monkeys[monkey.if_false].items.append(level)
            inspected_by_monkey[i] += 1
    return


def operate(operation: List[str], old: int):
    a, op, b = operation

    a = old if a == "old" else int(a)
    b = old if b == "old" else int(b)

    if op == "+":
        return a + b
    elif op == "*":
        return a * b


def parse(filename):
    monkeys = {}

    with open(filename) as f:
        blocks = f.read().split("\n\n")

        for block in blocks:
            lines = block.split("\n")
            id = int(lines[0].strip().removeprefix("Monkey ").rstrip(":"))
            items = deque(
                [
                    int(item)
                    for item in lines[1]
                    .strip()
                    .removeprefix("Starting items: ")
                    .split(",")
                ]
            )
            operation = lines[2].strip().removeprefix("Operation: new =").split()
            divisible_by = int(lines[3].strip().removeprefix("Test: divisible by "))
            if_true = int(lines[4].strip().removeprefix("If true: throw to monkey "))
            if_false = int(lines[5].strip().removeprefix("If false: throw to monkey "))
            monkeys[id] = Monkey(id, items, operation, divisible_by, if_true, if_false)
    return monkeys


def main():
    monkeys = parse("11/input.txt")
    inspected_by_monkey = simulate(deepcopy(monkeys), rounds=20)
    print(f"Part 1: {monkey_biz(inspected_by_monkey)}")
    inspected_by_monkey = simulate(deepcopy(monkeys), rounds=10_000, with_ease=False)
    print(f"Part 2: {monkey_biz(inspected_by_monkey)}")


if __name__ == "__main__":
    main()
