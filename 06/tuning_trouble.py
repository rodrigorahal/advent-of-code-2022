import fileinput


def find(stream, size=4):
    for i in range(size, len(stream)):
        window = stream[i - size : i]
        if len(window) == len(set(window)):
            return i


def parse():
    return [line.strip() for line in fileinput.input()]


def main():
    streams = parse()
    print(f"Part 1: {[find(stream, size=4) for stream in streams ]}")
    print(f"Part 1: {[find(stream, size=14) for stream in streams ]}")


if __name__ == "__main__":
    main()
