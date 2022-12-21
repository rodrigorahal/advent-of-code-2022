import fileinput
import operator
import math
from collections import defaultdict

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "=": operator.eq,
}


def topological_sort(graph):
    seen = set()
    order = []

    def dfs(node):
        if node in seen:
            return
        seen.add(node)
        for n in graph[node]:
            if n not in seen:
                dfs(n)
        order.append(node)

    for node in graph:
        dfs(node)
    return order


def calculate(graph, order, ops):
    res = dict()
    for node in order:
        if not graph[node]:
            res[node] = ops[node]
        else:
            a, op, b = ops[node]
            res[node] = OPS[op](res[a], res[b])
    a, b = graph["root"]
    return res["root"], (res[a], res[b])


def search(graph, order, ops, upper=9000000000000):
    ops["root"] = (ops["root"][0], "=", ops["root"][2])

    hi = upper
    lo = 0
    while lo <= hi:
        h = (hi + lo) // 2
        ops["humn"] = h
        found, (a, b) = calculate(graph, order, ops)
        if found:
            return h
        if a > b:
            lo = h + 1
        elif a <= b:
            hi = h - 1

    return -1


def parse():
    graph = defaultdict(list)
    ops = {}
    for line in fileinput.input():
        monkey, words = line.strip().split(": ")
        if len(words.split()) == 1:
            ops[monkey] = int(words)
            graph[monkey] = []
        elif len(words.split()) == 3:
            a, op, b = words.strip().split()
            ops[monkey] = (a, op, b)
            graph[monkey].extend([a, b])
    return ops, graph


def main():
    ops, graph = parse()
    order = topological_sort(graph)
    res, _ = calculate(graph, order, ops)
    print(f"Part 1: {int(res)}")
    print(f"Part 2: {search(graph, order, ops)}")


if __name__ == "__main__":
    main()
