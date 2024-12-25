import pathlib
from typing import List, Tuple
from functools import cache
from functools import lru_cache
import copy
import random

import time

# The expected solutions for the example input of the first part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 3
given_example_solution_of_second_part = "z00,z01,z02,z05"


class Lock:
    def __init__(self, input: str):
        self.heights = [0] * 5
        for height, line in enumerate(input.split("\n")):
            for index, character in enumerate(line):
                if character == "#":
                    self.heights[index] = height


class Key:
    def __init__(self, input: str):
        self.heights = [0] * 5
        for height, line in enumerate(reversed(input.split("\n"))):
            for index, character in enumerate(line):
                if character == "#":
                    self.heights[index] = height

    def fits(self, lock: Lock) -> bool:
        for key_height, lock_height in zip(self.heights, lock.heights):
            if key_height + lock_height > 5:
                return False
        return True


def solve_first_part(keys: List[Key], locks: List[Lock]) -> int:
    fits = 0
    for lock in locks:
        for key in keys:
            if key.fits(lock):
                fits += 1
    return fits


def solve_second_part(keys: List[Key], locks: List[Lock]) -> int:
    return 0


def parse(input: str) -> Tuple[List[Key], List[Lock]]:
    keys = []
    locks = []
    for block in input.split("\n\n"):
        if block.startswith("."):
            keys.append(Key(block))
        elif block.startswith("#"):
            locks.append(Lock(block))
    return keys, locks


def read_input_from_file(path: str) -> str | None:
    """Reads the input from a file and returns it as a string.

    Args:
        path: The path to the file to read.

    Returns:
        The content of the file as a string or None if the file was not found.
    """
    try:
        input = pathlib.Path(path).read_text().strip()
        return input
    except FileNotFoundError:
        print(f'ERROR: Input file "{path}" not found.')
    except Exception as exception:
        print(
            f'An unexpected error occurred while reading the input file "{path}": {exception}'
        )
    return None


def solve_part(
    example_keys,
    example_locks,
    keys,
    locks,
    solver: callable,
    given_solution: int,
) -> None:
    """Solves part of the puzzle after checking the solver using the example solution.

    Args:
        example: The example input used for checking.
        input: The actual input required for the current puzzle.
        solver: The function to solve the part of the puzzle.
        given_solution: The expected solution for the example input.
    """
    if solver is solve_first_part:
        begin = time.time()
        calculated_solution = solver(example_keys, example_locks)
        print(f"{time.time()-begin:.4f} seconds needed to solve the example input.")
        assert (
            calculated_solution == given_solution
        ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
        print("The solution for the example input was correctly reproduced.")

    begin = time.time()
    calculated_solution = solver(keys, locks)
    print(f"{time.time()-begin:.4f} seconds needed to solve the actual input.")
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_keys, example_locks = parse(example_input)
    keys, locks = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_keys,
        example_locks,
        keys,
        locks,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_keys,
        example_locks,
        keys,
        locks,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
