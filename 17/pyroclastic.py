import fileinput
from itertools import cycle

DIRS = {">": (0, 1), "<": (0, -1), "v": (-1, 0)}

ROCKS = {
    "-": lambda rc: [(rc[0], rc[1] + i) for i in range(4)],
    "+": lambda rc: [
        (rc[0] + 2, rc[1] + 1),
        (rc[0] + 1, rc[1]),
        (rc[0] + 1, rc[1] + 1),
        (rc[0] + 1, rc[1] + 2),
        (rc[0], rc[1] + 1),
    ],
    "l": lambda rc: [
        (rc[0], rc[1]),
        (rc[0], rc[1] + 1),
        (rc[0], rc[1] + 2),
        (rc[0] + 1, rc[1] + 2),
        (rc[0] + 2, rc[1] + 2),
    ],
    "|": lambda rc: [
        (rc[0], rc[1]),
        (rc[0] + 1, rc[1]),
        (rc[0] + 2, rc[1]),
        (rc[0] + 3, rc[1]),
    ],
    "[]": lambda rc: [
        (rc[0], rc[1]),
        (rc[0], rc[1] + 1),
        (rc[0] + 1, rc[1]),
        (rc[0] + 1, rc[1] + 1),
    ],
}


def simulate(grid, pattern, steps=2022):
    jet = cycle(pattern)
    height = 0

    for i in range(steps):
        rock = generate_rock(i, row=height + 4, col=2)
        # draw(grid, rock)
        while True:
            dir = DIRS[next(jet)]
            rock, _ = move(grid, rock, dir)
            rock, moved = move(grid, rock, DIRS["v"])
            if not moved:
                grid.update({(row, col): "#" for (row, col) in rock})
                prev_height = height
                height = max(prev_height, max(row for row, _ in rock))
                # generate a string of height increase to detect periodic pattern
                # print(f"{height-prev_height}", end="")
                break
    return grid, height


def move(grid, rock, dir):
    moved = []
    dr, dc = dir
    for row, col in rock:
        r, c = row + dr, col + dc
        if r < 0 or c < 0 or c > 6 or (r, c) in grid:
            return rock, False
        moved.append((r, c))
    return moved, True


def generate_rock(i, row, col):
    symbol = ["-", "+", "l", "|", "[]"][i % len(ROCKS)]
    return ROCKS[symbol]((row, col))


def edges(grid, rock):
    rs = [row for row, _ in grid]
    if rock:
        rs.extend([row for row, _ in rock])
    minrow, maxrow = 0, max(rs)
    mincol, maxcol = 0, 6
    return (minrow, maxrow), (mincol, maxcol)


def draw(grid, rock=None):
    if not grid:
        return

    (minrow, maxrow), (mincol, maxcol) = edges(grid, rock)

    for row in range(maxrow, minrow - 1, -1):
        line = ["|"]
        for col in range(mincol, maxcol + 1):
            if (row, col) in grid:
                line.append("#")
            elif rock is not None and (row, col) in rock:
                line.append("@")
            else:
                line.append(".")
        line.append("|")
        print("".join(line))
    print("+-------+")
    print()


def parse():
    return [char for char in fileinput.input().readline().strip()]


def main():
    pattern = parse()
    grid, maxrow = simulate(dict(), pattern, steps=2022)
    print(f"Part 1: {maxrow}")

    """
    manually detected a periodic sequence in the *increase in height*
    period only starts after an _initial_ state has settled
    after that it repeats with a certatin frequency of ~1720 steps/rocks
    """
    initial = "1234000340133221303003300022221222012142133000222200342132001322013022132021324213040021421332013322132221332213340020010302002220133001330013240003401324212242133021330012320133001334012300133000222002040130400201202200133001334213340132"
    period = "4212320123421330013200132400021003342033001330013340133001304013030132221013013211121220032203032103201322013200122400030212130133020032202242133221330213211130321212212110133021321213340130421332013222123401222012301130421320012122130301304213040133400031013322123000203013222133221330002340133401332013042121301332213200133001301201322133020220012222033201214013020132201330012220132021321002320133001330013212123001322013340132011214213220133201330212120033221321213240121201334012211033221330003020113021332002300032001330200302130220032212322133201320003220020221332013300132201324210002132201330003302123201332212342033201303012302121201330213220133001230012211130301330012122122020304202320121301332013222133000230013240133001330012122123201320013322122221302212340132201330013222132001302213340133001324012132022201322013340022111214002340003001212212140013201124013042123021212213320132001330013320133201330013300112111334002000121101212012300133201334013200132001222010220122221334012300132121213012122122001332003340133201322013300013400222012122133421321213302132201232013322133400010113300103200232012120030301304012120133400032013340133000203012220130121334012122123201320010322130201330213032133001332213340130301332212301133001213003210121221302213300130300234010340132201324213300133021322211240133001321112140132201234213340133400220013322132220030013300122420221113240132221222013240133401222012320121201332013220133201332013222133001212212120130421330013040121201324212320130301321012320133201004212300112201332013202003221321113042121401334002220133001212012340121300322213340132401301113220023401030013022132400030212320123021212013320022400030013320132001222013040130300230212342121221210212240133"
    frequency = len(period)

    total = 1000000000000
    remaining = total - len(initial)
    initial_height = sum([int(n) for n in initial])
    n, rest = divmod(remaining, frequency)
    periodic_height = sum([int(n) for n in period])

    height = initial_height + (n * periodic_height) + sum(int(n) for n in period[:rest])
    print(f"Part 2: {height}")


if __name__ == "__main__":
    main()
