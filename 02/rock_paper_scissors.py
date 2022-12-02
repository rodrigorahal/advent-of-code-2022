import fileinput


L = [("A", "Z"), ("C", "Y"), ("B", "X")]
W = [("A", "Y"), ("B", "Z"), ("C", "X")]
D = [("A", "X"), ("B", "Y"), ("C", "Z")]

score_by_play = {"X": 1, "Y": 2, "Z": 3}
score_by_outcome = {"W": 6, "D": 3, "L": 0}
outcome_by_play = {"X": "L", "Y": "D", "Z": "W"}


def simulate(rounds):
    score = 0
    for round in rounds:
        opponent, me = round
        score += score_by_outcome[get_outcome(round)] + score_by_play[me]
    return score


def simulate_by_outcome(rounds):
    score = 0
    for round in rounds:
        opponent, me = round
        score += score_by_outcome[outcome_by_play[me]] + score_by_play[get_play(round)]
    return score


def get_outcome(round):
    opponent, me = round

    if (opponent, me) in W:
        return "W"

    if (opponent, me) in L:
        return "L"

    return "D"


def get_play(round):
    opponent, play = round

    if outcome_by_play[play] == "L":
        return dict(L)[opponent]

    elif outcome_by_play[play] == "D":
        return dict(D)[opponent]

    elif outcome_by_play[play] == "W":
        return dict(W)[opponent]


def parse():
    return [line.strip().split(" ") for line in fileinput.input()]


def main():
    rounds = parse()
    score = simulate(rounds)
    print(f"Part 1: {score}")

    score = simulate_by_outcome(rounds)
    print(f"Part 2: {score}")


if __name__ == "__main__":
    main()
