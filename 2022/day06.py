#!/usr/bin/env python3

import argparse
import logging
import enum
from dataclasses import dataclass
from typing import Iterator, Collection


class MarkerTypes(enum.Enum):
    package = 4
    message = 14


@dataclass
class Signal:
    stream: str

    def _iter_markers(self, marker: MarkerTypes) -> Iterator[tuple[int, str]]:
        for start, end in enumerate(range(marker.value, len(self.stream))):
            yield end, self.stream[start:end]

    def marker_position(self, marker: MarkerTypes):
        for position, data in self._iter_markers(marker):
            if not includes_duplicates(data):
                return position


def convert_input_data(f):
    def convert(input_data):
        converted_input_data = []
        for entry in input_data:
            converted_input_data.append(Signal(entry))
        return f(converted_input_data)

    return convert


def includes_duplicates(data: Collection) -> bool:
    return len(data) != len(set(data))


@convert_input_data
def part1(signals: list[Signal]) -> list[int]:
    logging.debug(f"signals: {signals}")
    solutions: list[int] = []

    for signal in signals:
        solutions.append(signal.marker_position(MarkerTypes.package))

    return solutions


@convert_input_data
def part2(signals: list[Signal]) -> list[int]:
    solutions: list[int] = []

    for signal in signals:
        solutions.append(signal.marker_position(MarkerTypes.message))

    return solutions


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
