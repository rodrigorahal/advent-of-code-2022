import fileinput
from collections import defaultdict, deque
from itertools import combinations


def explore(graph, rates, start="AA", T=30):
    path = {start}
    open = set()
    t = 0
    pressure = 0
    queue = deque([(start, path, open, t, pressure)])
    max_pressure = float("-inf")

    while queue:
        curr, path, open, t, pressure = queue.popleft()

        if t >= T:
            max_pressure = max(max_pressure, pressure)
            continue

        # hack-101 for pruning... why not?!
        if t > 20 and pressure < 1000:
            continue

        if curr not in open and rates[curr] != 0:
            valve_pressure = (T - (t + 1)) * rates[curr]
            queue.append(
                (
                    curr,
                    {curr},  # when we open a valve we can backtrack
                    open | {curr},
                    t + 1,
                    pressure + valve_pressure,
                )
            )
        for valve in graph[curr]:
            # no backtracking unless we open a valve
            if valve not in path:
                queue.append((valve, path | {valve}, open | set(), t + 1, pressure))

    return max_pressure


def distances(graph):
    dists = dict()
    for start, end in combinations(graph.keys(), 2):
        dists[(start, end)] = bfs(graph, start, end)
        dists[(end, start)] = bfs(graph, end, start)
    return dists


def bfs(graph, start, end):
    seen = set()
    queue = deque([(start, 0)])
    while queue:
        curr, steps = queue.popleft()
        if curr in seen:
            continue
        seen.add(curr)
        if curr == end:
            return steps
        for valve in graph[curr]:
            queue.append((valve, steps + 1))
    return -1


def reachable(graph, rates, dists, start="AA", T=30):
    can_open_valves = [valve for valve, rate in rates.items() if rate > 0]
    pressures = []
    stack = [(start, set(), 0, 0)]

    while stack:
        curr, path, t, pressure = stack.pop()

        can_reach = [
            valve
            for valve in can_open_valves
            if valve != curr and valve not in path and dists[(valve, curr)] < T - t - 1
        ]

        if not can_reach:
            pressures.append((pressure, path))
            continue

        for valve in can_reach:
            d = dists[(valve, curr)]
            valve_pressure = (T - d - t - 1) * rates[valve]
            stack.append((valve, path | {valve}, t + d + 1, pressure + valve_pressure))
    return pressures


def match(solutions):
    max_pressure = 0
    for (pressure1, path1), (pressure2, path2) in combinations(solutions, 2):
        if pressure1 + pressure2 < max_pressure:
            continue
        if not path1.intersection(path2):
            max_pressure = max(max_pressure, pressure1 + pressure2)
    return max_pressure


def parse():
    graph = defaultdict(list)
    rates = dict()
    for line in fileinput.input():
        words = line.strip()[6:].split("; ")
        valve, rate = words[0].split(" has flow rate=")
        valve = valve.strip()
        rate = int(rate)
        tunnels = words[1].strip().strip("tunnel leads to valve ").split(", ")
        graph[valve].extend(tunnels)
        rates[valve] = rate
    return graph, rates


def main():
    graph, rates = parse()
    # naively explore
    max_pressure = explore(graph, rates)
    print(f"Part 1 naive: {max_pressure}")
    dists = distances(graph)
    solutions = reachable(graph, rates, dists)
    print(f"Part 1: {max(pressure for pressure, _ in solutions)}")
    solutions = reachable(graph, rates, dists, T=26)
    print(f"Part 2: {match(solutions)}")


if __name__ == "__main__":
    main()
