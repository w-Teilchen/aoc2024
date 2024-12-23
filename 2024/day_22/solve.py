import pathlib
from typing import List
import sys
import copy
import time

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 37990510
given_example_solution_of_second_part = 23


def parse(input: str) -> List[int]:
    return [int(number) for number in input.splitlines()]


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(a: int) -> int:
    return a % 16777216


def get_next_numbers(secret_numbers: List[int]) -> None:
    for index, secret_number in enumerate(secret_numbers):
        secret_number = mix(secret_number, 64 * secret_number)
        secret_number = prune(secret_number)
        secret_number = mix(secret_number, int(secret_number / 32))
        secret_number = prune(secret_number)
        secret_number = mix(secret_number, secret_number * 2048)
        secret_number = prune(secret_number)
        secret_numbers[index] = secret_number

    return None


def solve_first_part(secret_numbers: List[int]) -> int:
    for _ in range(2000):
        get_next_numbers(secret_numbers)

    return sum(secret_numbers)


def sum_up(sequences: List[dict[str, int]]) -> dict[str, int]:
    sums = copy.deepcopy(sequences[0])
    for sequence in sequences[1:]:
        for key, value in sequence.items():
            if key in sums:
                sums[key] += value
            else:
                sums[key] = value
    return sums


def solve_second_part(secret_numbers: List[int]) -> int:
    differences = []
    previous_secret_numbers = []
    for iteration in range(2000):
        previous_secret_numbers.append(copy.deepcopy(secret_numbers))
        get_next_numbers(secret_numbers)
        differences.append(
            [
                (a % 10) - (b % 10)
                for a, b in zip(secret_numbers, previous_secret_numbers[-1])
            ]
        )
    previous_secret_numbers.append(copy.deepcopy(secret_numbers))
    sequences = [{} for _ in range(len(secret_numbers))]
    for iteration, iterations_secret_numbers in enumerate(previous_secret_numbers):
        if iteration < 4:
            continue
        for index, secret_number in enumerate(iterations_secret_numbers):
            sequence = f"{differences[iteration-4][index]},{differences[iteration-3][index]},{differences[iteration-2][index]},{differences[iteration-1][index]}"
            if sequence not in sequences[index]:
                sequences[index][sequence] = secret_number % 10
    sums = sum_up(sequences)
    return max(sums.values())


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


def solve_part(example, input, solver: callable, given_solution: int) -> None:
    """Solves part of the puzzle after checking the solver using the example solution.

    Args:
        example: The example input used for checking.
        input: The actual input required for the current puzzle.
        solver: The function to solve the part of the puzzle.
        given_solution: The expected solution for the example input.
    """
    begin = time.time()
    calculated_solution = solver(example)
    print(f"{time.time()-begin} seconds needed to solve the example input.")
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    begin = time.time()
    calculated_solution = solver(input)
    print(f"{time.time()-begin} seconds needed to solve the actual input.")
    print(f"The solution to the input is {calculated_solution}")


def main():
    sys.setrecursionlimit(10000)

    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_numbers = parse(example_input)
    original_example_numbers = copy.deepcopy(example_numbers)
    numbers = parse(input)
    original_numbers = copy.deepcopy(numbers)

    print("\nSolving first part...")
    solve_part(
        example_numbers,
        numbers,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        original_example_numbers,
        original_numbers,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
