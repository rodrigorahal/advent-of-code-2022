import fileinput


def scanned(report, row):
    xs = set()
    for sensor, beacon, dist in report:
        sx, sy = sensor
        if abs(row - sy) > dist:
            continue
        diff = dist - abs(row - sy)
        for x in range(sx - diff, sx + diff + 1):
            if (x, row) != beacon:
                xs.add(x)
    return xs


def scanned_ranges(report, row, bounds):
    minx, maxx = bounds
    ranges = []
    for sensor, beacon, dist in report:
        sx, sy = sensor
        if abs(row - sy) > dist:
            continue
        diff = dist - abs(row - sy)
        xleft = max(sx - diff, minx)
        xright = min(sx + diff, maxx)
        ranges.append((xleft, xright))
    return sorted(ranges)


def merge(ranges):
    merged = [ranges[0]]
    for range in ranges[1:]:
        (astart, aend), (bstart, bend) = merged[-1], range
        if can_merge(merged[-1], range):
            merged[-1] = astart, max(aend, bend)
        else:
            merged.append(range)
    return merged


def can_merge(a, b):
    """
    as ------ ae
        bs ------ be
    """
    astart, aend = a
    bstart, bend = b
    return astart <= bstart <= aend + 1


def find(report, bounds):
    miny, maxy = bounds
    for row in range(miny, maxy + 1):
        ranges = scanned_ranges(report, row, bounds)
        merged = merge(ranges)
        if len(merged) > 1:
            (_, aend), _ = merged
            return aend + 1, row


def distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(bx - ax) + abs(by - ay)


def parse():
    report = []
    for line in fileinput.input():
        sensor, beacon = line.strip().split(": ")
        sensorx, sensory = sensor.removeprefix("Sensor at ").split(", ")
        sensor = (int(sensorx[2:]), int(sensory[2:]))
        beaconx, beacony = beacon.removeprefix("closest beacon is at ").split(", ")
        beacon = (int(beaconx[2:]), int(beacony[2:]))
        report.append((sensor, beacon, distance(sensor, beacon)))
    return report


def main():
    report = parse()
    xs = scanned(report, row=2_000_000)
    print(f"Part 1: {len(xs)}")
    x, y = find(report, bounds=(0, 4_000_000))
    print(f"Part 2: {x * 4_000_000 + y}")


if __name__ == "__main__":
    main()
