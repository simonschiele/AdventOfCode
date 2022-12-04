#!/usr/bin/env python3

import argparse
import logging


def convert_input_data(f):
    def convert(input_data):
        converted_input_data = []
        for entry in input_data:
            x, y = entry.split(',')

            x = list(map(int, x.split('-')))
            x[1] += 1
            x = set(range(*x))

            y = list(map(int, y.split('-')))
            y[1] += 1
            y = set(range(*y))

            converted_input_data.append((x, y))
        return f(converted_input_data)
    return convert


@convert_input_data
def part1(input_data: list[tuple[set[int], set[int]]]) -> int:
    contains = 0
    for input_line, (x, y) in enumerate(input_data):
        logging.debug(f"part1 | {input_line}: {x} <-> {y}")
        if x.issubset(y) or y.issubset(x):
            contains += 1

    return contains


@convert_input_data
def part2(input_data: list[tuple[set[int], set[int]]]) -> int:
    overlaps = 0
    for input_line, (x, y) in enumerate(input_data):
        logging.debug(f"part2 | {input_line}: {x} <-> {y}")
        if x.intersection(y):
            overlaps += 1

    return overlaps


if __name__ == "__main__":
    default_input_filename = f"input_{__file__[-5:-3]}.txt"
    input_data: dict[str, list[str]] = {}

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument(
        'input_files',
        nargs='*',
        default=[f"test_{default_input_filename}", default_input_filename]
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
