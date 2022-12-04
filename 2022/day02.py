#!/usr/bin/env python3

import argparse
import dataclasses
import enum
import logging


class Shape(enum.Enum):
    rock = enum.auto()
    paper = enum.auto()
    scissors = enum.auto()


class GameOutcome(enum.Enum):
    lost = 0
    draw = 3
    won = 6


shape_mapping = {
    "A": Shape.rock,
    "B": Shape.paper,
    "C": Shape.scissors,
    "X": Shape.rock,
    "Y": Shape.paper,
    "Z": Shape.scissors,
}

win_mapping = {
    Shape.rock: Shape.scissors,
    Shape.paper: Shape.rock,
    Shape.scissors: Shape.paper,
}

expected_outcome_mapping = {
    "X": GameOutcome.lost,
    "Y": GameOutcome.draw,
    "Z": GameOutcome.won,
}


@dataclasses.dataclass
class Game:
    oponnents_choice: Shape
    my_choice: Shape

    def outcome(self):
        if self.my_choice == self.oponnents_choice:
            return GameOutcome.draw
        elif win_mapping[self.my_choice] == self.oponnents_choice:
            return GameOutcome.won
        else:
            return GameOutcome.lost

    @classmethod
    def by_outcome(cls, oponnents_choice, expected_outcome):
        if expected_outcome == GameOutcome.draw:
            my_choice = oponnents_choice
        elif expected_outcome == GameOutcome.lost:
            my_choice = win_mapping[oponnents_choice]
        else:
            lose_mapping = dict(map(reversed, win_mapping.items()))
            my_choice = lose_mapping[oponnents_choice]

        return cls(oponnents_choice, my_choice)


def convert_input_data(f):
    def convert(input_data):
        converted_input_data = []
        for entry in input_data:
            x, y = entry.split(" ")
            converted_input_data.append((x, y))
        return f(converted_input_data)

    return convert


@convert_input_data
def part1(input_data):
    points = 0

    for x, y in input_data:
        oponnents_choice = shape_mapping[x]
        my_choice = shape_mapping[y]

        game = Game(oponnents_choice, my_choice)
        points += game.my_choice.value
        points += game.outcome().value

    return points


@convert_input_data
def part2(input_data):
    points = 0

    for x, y in input_data:
        oponnents_choice = shape_mapping[x]
        expected_outcome = expected_outcome_mapping[y]

        game = Game.by_outcome(oponnents_choice, expected_outcome)
        points += game.my_choice.value
        points += game.outcome().value

    return points


if __name__ == "__main__":
    default_input_filename = f"input_{__file__[-5:-3]}.txt"
    input_data: dict[str, list[str]] = {}

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument(
        "input_files",
        nargs="*",
        default=[f"test_{default_input_filename}", default_input_filename],
    )
    args = parser.parse_args()

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logging.basicConfig(level=loglevel)
    logging.debug(f"input files: {args.input_files}")

    for filename in args.input_files:
        input_data[filename] = [line.strip() for line in open(filename)]

    for input_file, data in input_data.items():
        logging.info(f"PART1 ({input_file}) | solution: {part1(data)}")
        logging.info(f"PART2 ({input_file}) | solution: {part2(data)}")
