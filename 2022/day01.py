#!/usr/bin/env python3

import argparse
import logging


def main(input_data: list[str]) -> tuple[int, int]:
    calories: list[int] = [0]

    for entry in input_data:
        if entry:
            calories[-1] += int(entry)
        else:
            calories.append(0)

    return max(calories), sum(sorted(calories)[-3:])


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
        part1, part2 = main(data)
        logging.info(f"PART1 ({input_file}) | solution: {part1}")
        logging.info(f"PART2 ({input_file}) | solution: {part2}")
