import fileinput
import re
from collections import deque, defaultdict
from functools import reduce
from operator import mul


MATERIALS = ["ore", "clay", "obsidian", "geode"]


def quality_level(blueprints, T=24):
    return sum(
        blueprint["id"] * search(blueprint, defaultdict(int, ore=1), defaultdict(int))
        for blueprint in blueprints
    )


def product(blueprints, T=32):
    return reduce(
        mul,
        [
            search(blueprint, defaultdict(int, ore=1), defaultdict(int), T=32)
            for blueprint in blueprints
        ],
    )


def search(blueprint, robots, inventory, T=24):
    t = 0
    queue = deque([(robots, inventory, t)])
    geodes = 0
    seen = set()

    while queue:
        robots, inventory, t = queue.popleft()

        if t >= T:
            geodes = max(geodes, inventory["geode"])
            continue

        for i, material in enumerate(MATERIALS[:-1]):
            # prune execess robots
            max_cost = max(blueprint[m][i] for m in MATERIALS)
            robots[material] = min(robots[material], max_cost)

            # prune execess inventory
            max_inventory = (T - t) * max_cost - robots[material] * (T - t - 1)
            inventory[material] = min(inventory[material], max_inventory)

        frobots = frozendict(robots)
        finventory = frozendict(inventory)

        if (frobots, finventory, t) in seen:
            continue

        seen.add((frobots, finventory, t))

        for robot in reversed(MATERIALS):
            if (
                inventory["ore"] >= blueprint[robot][0]
                and inventory["clay"] >= blueprint[robot][1]
                and inventory["obsidian"] >= blueprint[robot][2]
            ):

                updated_inventory = update_inventory(inventory, robots)
                updated_robots = defaultdict(int, **robots)
                updated_robots[robot] += 1
                updated_inventory["ore"] -= blueprint[robot][0]
                updated_inventory["clay"] -= blueprint[robot][1]
                updated_inventory["obsidian"] -= blueprint[robot][2]

                queue.append((updated_robots, updated_inventory, t + 1))

                if robot == "geode":
                    break

        else:
            # dont build any robots
            updated_inventory = update_inventory(inventory, robots)
            queue.append((defaultdict(int, **robots), updated_inventory, t + 1))
    return geodes


def frozendict(d):
    return tuple((k, d[k]) for k in sorted(MATERIALS))


def update_inventory(inventory, robots):
    updated_inventory = defaultdict(int, **inventory)
    for robot, qty in robots.items():
        updated_inventory[robot] += qty
    return updated_inventory


def parse():
    blueprints = []
    for line in fileinput.input():
        nums = list(map(int, re.findall(r"\d+", line)))
        blueprints.append(
            {
                "id": nums[0],
                "ore": (nums[1], 0, 0),
                "clay": (nums[2], 0, 0),
                "obsidian": (nums[3], nums[4], 0),
                "geode": (nums[5], 0, nums[6]),
            }
        )
    return blueprints


def main():
    blueprints = parse()
    print(f"Part 1: {quality_level(blueprints)}")
    print(f"Part 2: {product(blueprints[:3])}")


if __name__ == "__main__":
    main()
