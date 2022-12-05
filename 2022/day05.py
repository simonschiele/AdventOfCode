#!/usr/bin/env python3

import argparse
import logging
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Instruction:
    quantity: int
    source: int
    target: int


@dataclass
class Crate:
    name: str


@dataclass
class Supplies:
    stacks: defaultdict[list[Crate]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def move(self, instruction: Instruction, cratemover=9000):
        crates_to_move = []
        for _ in range(instruction.quantity, 0, -1):
            crate_to_move = self.stacks[instruction.source].pop()
            if cratemover == 9000:
                crates_to_move.append(crate_to_move)
            elif cratemover == 9001:
                crates_to_move.insert(0, crate_to_move)
            else:
                raise NotImplementedError(
                    f"Cratemover {cratemover} not supported!"
                )

        self.stacks[instruction.target] += crates_to_move

    @property
    def top_crates(self):
        top_crates_string = ""

        for idx in range(1, len(self.stacks) + 1):
            top_crates_string += self.stacks[idx][-1].name

        return top_crates_string


def convert_input_data(f):
    def convert(input_data):
        instructions = []
        supplies = Supplies()

        for entry in input_data:
            if "[" in entry:
                for i, v in enumerate(entry[1::4], start=1):
                    if not v.isspace():
                        supplies.stacks[i].insert(0, Crate(v))
            elif entry.startswith("move"):
                _, one, _, two, _, three = entry.split()
                instruction = Instruction(*map(int, [one, two, three]))
                instructions.append(instruction)

        return f(supplies, instructions)

    return convert


@convert_input_data
def part1(supplies: Supplies, instructions: list[Instruction]) -> str:
    logging.debug(f"instructions: {instructions}")
    logging.debug(f"supplies: {supplies}")

    for instruction in instructions:
        supplies.move(instruction)

    return supplies.top_crates


@convert_input_data
def part2(supplies: Supplies, instructions: list[Instruction]) -> str:
    for instruction in instructions:
        supplies.move(instruction, cratemover=9001)

    return supplies.top_crates


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
        input_data[filename] = [line for line in open(filename)]

    for input_file, data in input_data.items():
        logging.info(f"PART1 ({input_file}) | solution: {part1(data)}")
        logging.info(f"PART2 ({input_file}) | solution: {part2(data)}")
