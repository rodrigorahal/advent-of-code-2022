from __future__ import annotations
import fileinput
from dataclasses import dataclass
from typing import List, Set


@dataclass
class Node:
    num: int
    next: Node = None
    prev: Node = None


def decrypt(sequence: List[Node], key: int = None, rounds: int = 10):
    for _ in range(rounds):
        mix(sequence, key)


def mix(sequence: List[Node], key: int = None):
    size = len(sequence)
    for node in sequence:
        move(node, size, key)


def grove(sequence: List[Node], coords: Set[int] = None, key: int = None):
    [zero] = [node for node in sequence if node.num == 0]

    i = s = 0
    curr = zero
    while i <= max(coords):
        if i in coords:
            s += curr.num if not key else curr.num * key
        curr = curr.next
        i += 1
    return s


def move(node: Node, size: int, key: int = None):
    steps = node.num if not key else (abs(node.num) * key) % (size - 1)

    if steps == 0:
        return

    if node.num > 0:
        node.prev.next = node.next
        node.next.prev = node.prev
        curr = node
        for _ in range(steps):
            curr = curr.next

        next = curr.next
        curr.next = node
        node.prev = curr
        node.next = next
        next.prev = node

    elif node.num < 0:
        prev = node.next
        next = node.prev
        prev.prev = next
        next.next = prev
        curr = node
        for _ in range(abs(steps)):
            curr = curr.prev

        next = curr.prev
        next.next = node
        node.prev = next
        node.next = curr
        curr.prev = node
    return


def make_ring(nums: List[int]):
    head = Node(nums[0])
    sequence = [head]
    prev = head
    for num in nums[1:]:
        curr = Node(num)
        curr.prev = prev
        prev.next = curr
        prev = curr
        sequence.append(curr)
    curr.next = head
    head.prev = curr
    return sequence


def print_ring(head: Node, size: int, key: int = None):
    curr = head
    nums = []
    for _ in range(size):
        nums.append(curr.num if not key else curr.num * key)
        curr = curr.next
    print(nums)


def parse():
    return [int(line.strip()) for line in fileinput.input()]


def main():
    nums = parse()
    sequence = make_ring(nums)
    mix(sequence)
    print(f"Part 1: {grove(sequence, coords={1000, 2000, 3000})}")

    sequence = make_ring(nums)
    KEY = 811589153
    decrypt(sequence, key=KEY, rounds=10)
    print(f"Part 2: {grove(sequence, coords={1000, 2000, 3000}, key=KEY)}")


if __name__ == "__main__":
    main()
