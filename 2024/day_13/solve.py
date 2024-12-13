import pathlib
from typing import List
import numpy as np
import re

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 480
given_example_solution_of_second_part = 875318608908


class ClawMachine:
    def __init__(self, button_configuration: np.ndarray, prize_location: List[int]):
        self.button_configuration = button_configuration
        self.prize_location = prize_location

    def get_prize(self) -> np.ndarray:
        if abs(np.linalg.det(self.button_configuration)) <= 1e-6:
            print("The matrix is singular.")
            return np.array(
                [0, self.prize_location[1] / self.button_configuration[1, 1]]
            )
        return np.linalg.solve(self.button_configuration, self.prize_location)


def parse(input: str):
    claw_machines = []

    lines = input.splitlines()
    blocks = [lines[i : i + 4] for i in range(0, len(lines), 4)]
    for block in blocks:
        matrix = np.zeros((2, 2))
        prize_location = np.zeros(2)
        for line in block:
            if "Button A:" in line:
                # use pattern matching to extract the numbers from "Button A: X+94, Y+34"
                numbers = [int(s) for s in re.findall(r"\d+", line)]
                matrix[0, 0] = numbers[0]
                matrix[1, 0] = numbers[1]
            elif "Button B:" in line:
                numbers = [int(s) for s in re.findall(r"\d+", line)]
                matrix[0, 1] = numbers[0]
                matrix[1, 1] = numbers[1]
            elif "Prize:" in line:
                numbers = [int(s) for s in re.findall(r"\d+", line)]
                prize_location[0] = numbers[0]
                prize_location[1] = numbers[1]
        claw_machines.append(ClawMachine(matrix, prize_location))

    return claw_machines


def solve_first_part(claw_machines) -> int:
    cost_of_button_presses = np.array([3, 1])
    total_cost = 0
    for claw_machine in claw_machines:
        necessary_button_presses = np.round(claw_machine.get_prize()).astype(int)
        if (
            np.linalg.norm(
                (
                    claw_machine.button_configuration @ necessary_button_presses
                    - claw_machine.prize_location
                )
            )
            < 1e-6
        ):
            total_cost += np.dot(cost_of_button_presses, necessary_button_presses)

    return total_cost


def solve_second_part(claw_machines) -> int:
    cost_of_button_presses = np.array([3, 1])
    total_cost = 0
    for claw_machine in claw_machines:
        claw_machine.prize_location += 10000000000000
        raw_result = claw_machine.get_prize()
        necessary_button_presses = (raw_result + 1e-4).astype(np.uint64)
        distance_to_prize = np.linalg.norm(
            (
                claw_machine.button_configuration @ necessary_button_presses
                - claw_machine.prize_location
            )
        )
        if distance_to_prize < 1e-6:
            total_cost += np.dot(cost_of_button_presses, necessary_button_presses)

    return int(total_cost)


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
    calculated_solution = solver(example)
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(input)
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    parsed_example = parse(example_input)
    parsed_input = parse(input)

    print("\nSolving first part...")
    solve_part(
        parsed_example,
        parsed_input,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        parsed_example,
        parsed_input,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
