import pathlib
from typing import List, Tuple
from functools import cache
from functools import lru_cache
import copy

import time

# The expected solutions for the example input of the first part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 126384


class Keypad:
    def __init__(self, input: str):
        rows = input.strip().split("\n")
        row_length = max([len(row) for row in rows])
        self.keypad = []
        for row in rows:
            self.keypad.append(list(row.rjust(row_length, " ")))

    @cache
    def get_keys_coordinate(self, key: str) -> Tuple[int, int]:
        for y, row in enumerate(self.keypad):
            for x, cell in enumerate(row):
                if cell == key:
                    return (x, y)
        raise ValueError(f"Key {key} not found on the keypad.")

    @cache
    def get_sequence_between_keys(self, start: str, end: str) -> List[str]:
        return self.get_sequence_between_coordinates(
            self.get_keys_coordinate(start), self.get_keys_coordinate(end)
        )

    @cache
    def get_sequence_between_coordinates(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> List[str]:
        vertical_direction = "v" if end[1] > start[1] else "^"
        horizontal_direction = ">" if end[0] > start[0] else "<"
        if start == end:
            return ["A"]
        if start[0] == end[0]:
            return [vertical_direction * abs(end[1] - start[1]) + "A"]
        if end[1] == start[1]:
            return [horizontal_direction * abs(end[0] - start[0]) + "A"]
        horizontal_distance = abs(end[0] - start[0])
        vertical_distance = abs(end[1] - start[1])
        combinations = copy.deepcopy(
            get_all_combinations(
                horizontal_distance,
                horizontal_direction,
                vertical_distance,
                vertical_direction,
            )
        )
        buttons_to_reach_coordinate = []
        for combination in combinations:
            doesnt_move_over_empty_key = True
            intermediate_position = start
            for key in combination:
                if key == "^":
                    intermediate_position = (
                        intermediate_position[0],
                        intermediate_position[1] - 1,
                    )
                elif key == "v":
                    intermediate_position = (
                        intermediate_position[0],
                        intermediate_position[1] + 1,
                    )
                elif key == "<":
                    intermediate_position = (
                        intermediate_position[0] - 1,
                        intermediate_position[1],
                    )
                elif key == ">":
                    intermediate_position = (
                        intermediate_position[0] + 1,
                        intermediate_position[1],
                    )
                elif key == "A":
                    break
                else:
                    raise ValueError(f'Unknown key "{key}" found in generated path.')
                if (
                    self.keypad[intermediate_position[1]][intermediate_position[0]]
                    == " "
                ):
                    doesnt_move_over_empty_key = False
                    break
            if doesnt_move_over_empty_key:
                buttons_to_reach_coordinate.append(combination + "A")
        return buttons_to_reach_coordinate


numerical_keys = "1234567890A"
numerical_keypad = Keypad("789\n456\n123\n0A")

directional_keys = "^v<>A"
directional_keypad = Keypad("^A\n<v>")


@cache
def get_all_combinations(n: int, first: str, m: int, second: str) -> List[str]:
    if n == 1 and m == 0:
        return [first]
    if n == 0 and m == 1:
        return [second]
    combinations = []
    if n > 0:
        combinations += [
            first + combination
            for combination in get_all_combinations(n - 1, first, m, second)
        ]
    if m > 0:
        combinations += [
            second + combination
            for combination in get_all_combinations(n, first, m - 1, second)
        ]

    return combinations


@cache
def find_sequences_to_get_from_start_to_end(start: str, end: str) -> List[str]:
    if start == end:
        return ["A"]
    if start in directional_keys and end in directional_keys:
        return directional_keypad.get_sequence_between_keys(start, end)
    if start in numerical_keys and end in numerical_keys:
        return numerical_keypad.get_sequence_between_keys(start, end)
    raise ValueError(f'"{start}" and "{end}" are not on the same keypad.')


@cache
def calculate_number_of_buttons_to_press(code: str, remaining_iterations: int) -> int:
    if remaining_iterations == 0:
        return len(code)
    buttons_to_press = 0
    for start, end in zip("A" + code, code):
        sequences = find_sequences_to_get_from_start_to_end(start, end)
        buttons_to_press += min(
            calculate_number_of_buttons_to_press(sequence, remaining_iterations - 1)
            for sequence in sequences
        )
    return buttons_to_press


def solve_first_part(
    codes: List[str],
) -> int:
    complexity = 0
    for code in codes:
        value = int(code[:-1])
        length = calculate_number_of_buttons_to_press(code, 3)
        complexity += length * value

    return complexity


def solve_second_part(
    codes: List[str],
) -> int:
    complexity = 0
    for code in codes:
        value = int(code[:-1])
        length = calculate_number_of_buttons_to_press(code, 26)
        complexity += length * value

    return complexity


def parse(input: str) -> List[str]:
    return input.splitlines()


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
    example,
    input,
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
        calculated_solution = solver(example)
        print(f"{time.time()-begin:.4f} seconds needed to solve the example input.")
        assert (
            calculated_solution == given_solution
        ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
        print("The solution for the example input was correctly reproduced.")

    begin = time.time()
    calculated_solution = solver(input)
    print(f"{time.time()-begin:.4f} seconds needed to solve the actual input.")
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_codes = parse(example_input)
    codes = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_codes,
        codes,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_codes,
        codes,
        solve_second_part,
        0,
    )


if __name__ == "__main__":
    main()
