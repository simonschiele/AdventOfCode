#!/usr/bin/env python3

from __future__ import annotations

import argparse
import logging
import dataclasses
from string import ascii_lowercase, ascii_uppercase

points_mapping = {
    v: i for i, v in enumerate(ascii_lowercase + ascii_uppercase, start=1)
}


@dataclasses.dataclass
class Backpacks:
    backpacks: list[Backpack]

    @classmethod
    def by_str_list(cls, backpack_strings: list[str]) -> Backpacks:
        backpacks = [Backpack(content) for content in backpack_strings]
        return cls(backpacks)

    def slices(self, amount=3):
        start, end = 0, 0
        while end < len(self.backpacks):
            start = end
            end += amount
            yield self.backpacks[start:end]


@dataclasses.dataclass
class Backpack:
    content: str

    @property
    def compartments(self):
        middle = len(self.content) // 2
        return (self.content[:middle], self.content[middle:])

    def search_wrongly_sorted_items(self):
        compartment1, compartment2 = self.compartments
        wrong_items = []

        for thing in compartment1:
            if thing in wrong_items:
                continue

            if thing in compartment2:
                wrong_items.append(thing)

        return wrong_items


def convert_input_data(f):
    def convert(input_data):
        backpacks = Backpacks.by_str_list(input_data)
        return f(backpacks)

    return convert


@convert_input_data
def part1(input_data: Backpacks) -> int:
    points = 0

    for backpack in input_data.backpacks:
        for thing in backpack.search_wrongly_sorted_items():
            points += points_mapping[thing]

    return points


@convert_input_data
def part2(input_data: Backpacks) -> int:
    points = 0

    for next_backpacks in input_data.slices(3):
        for thing in next_backpacks.pop().content:
            if all(thing in backpack.content for backpack in next_backpacks):
                points += points_mapping[thing]
                break

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
