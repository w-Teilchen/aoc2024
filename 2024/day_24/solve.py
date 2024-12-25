import pathlib
from typing import List, Tuple
import sys

import time
import sys

# The expected solutions for the example input of the first part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 2024
given_example_solution_of_second_part = "z00,z01,z02,z05"


def evaluate(
    output: str,
    initial_values: dict[str, int],
    operations: dict[Tuple[str, str, str]],
) -> dict[str, int]:
    if output in initial_values:
        return initial_values[output]
    a, b, operation = operations[output]
    a = evaluate(a, initial_values, operations)
    b = evaluate(b, initial_values, operations)
    if operation == "AND":
        return a & b
    if operation == "OR":
        return a | b
    if operation == "XOR":
        return a ^ b

    raise ValueError(f"Unknown operation: {operation}")


def solve_first_part(
    initial_values: dict[str, int], operations: dict[Tuple[str, str, str]]
) -> int:
    target_value = 0
    for digit in range(max([int(key[1:]) for key in operations.keys() if "z" in key])):
        z = f"z{digit:02}"
        target_value += evaluate(z, initial_values, operations) * 2**digit
    return target_value


def swap(
    a: str,
    b: str,
    operations_by_input: dict[Tuple[str, str, str]],
    operations_by_output: dict[Tuple[str, str, str]],
) -> None:
    operations_by_output[a], operations_by_output[b] = (
        operations_by_output[b],
        operations_by_output[a],
    )
    # As operations_by_output have already been swapped, we need to just assign a and b:
    (
        operations_by_input[operations_by_output[a]],
        operations_by_input[operations_by_output[b]],
    ) = (a, b)


# This solution only works for ADDITION, not AND as in the example.
def solve_second_part(
    _ignored: any, operations_by_output: dict[Tuple[str, str, str]]
) -> str:
    # This dict is used to look up the variable names used in input.txt.
    operations_by_input = {
        (operation[0], operation[1], operation[2]): key
        for key, operation in operations_by_output.items()
    }

    improvements = set()
    # Idea: Walk through the digits and check if the operations are correct. Each digit is calculated as xor from the two inputs and the overflow from the previous digit.
    for digit in range(
        max([int(key[1:]) for key in operations_by_output.keys() if "z" in key])
    ):
        x = f"x{digit:02}"
        y = f"y{digit:02}"
        z = f"z{digit:02}"
        if (
            digit == 0
        ):  # Get the variable name of the overflow from first to second digit:
            overflow = operations_by_input[(x, y, "AND")]
            continue
        # Look for the operation that calculates the current digit of z (from x, y and the previous overflow):
        x_xor_y = operations_by_input[(x, y, "XOR")]
        a, b = sorted([overflow, x_xor_y])
        if (a, b, "XOR") not in operations_by_input:
            # In this case a or b have the wrong name -> swap them with the inputs for the current digit of z:
            swapped_variables = list(set(operations_by_output[z][:2]) ^ set((a, b)))
            improvements.update(swapped_variables)
            swap(*swapped_variables, operations_by_input, operations_by_output)
        elif operations_by_input[a, b, "XOR"] != z:
            # In this case the output of a xor b is not the current digit of z -> swap its output with whatever outputs to z:
            improvements.add(operations_by_input[a, b, "XOR"])
            improvements.add(z)
            swap(
                operations_by_input[a, b, "XOR"],
                z,
                operations_by_input,
                operations_by_output,
            )
        # Find the overflow to the next digit (from input.txt this is (x xor y and previous overflow) OR (x AND y)):
        x_xor_y = operations_by_input[(x, y, "XOR")]
        overflow = operations_by_input[*sorted([overflow, x_xor_y]), "AND"]
        # If x and y or the previously calculated potential overflow are 1, the digit will overflow:
        x_and_y = operations_by_input[(x, y, "AND")]
        overflow = operations_by_input[*sorted([overflow, x_and_y]), "OR"]

    return ",".join(sorted(improvements))


def get_bit_at_position(number: int, position: int) -> int:
    return (number >> position) & 1


def parse(input: str) -> Tuple[dict[str, int], dict[Tuple[str, str, str]]]:
    initial_values = {}
    for line in input.split("\n\n")[0].splitlines():
        variable, value = line.split(": ")
        initial_values[variable] = int(value)
    operations = {}
    for line in input.split("\n\n")[1].splitlines():
        parts = line.split(" ")
        inputs = sorted([parts[0], parts[2]])  # sort for second part
        operation = parts[1]
        output = parts[-1]
        operations[output] = inputs[0], inputs[1], operation
    return (initial_values, operations)


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
    example_initial_values,
    example_operations,
    initial_values,
    operations,
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
        calculated_solution = solver(example_initial_values, example_operations)
        print(f"{time.time()-begin:.4f} seconds needed to solve the example input.")
        assert (
            calculated_solution == given_solution
        ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
        print("The solution for the example input was correctly reproduced.")

    begin = time.time()
    calculated_solution = solver(initial_values, operations)
    print(f"{time.time()-begin:.4f} seconds needed to solve the actual input.")
    print(f"The solution to the input is {calculated_solution}")


def main():
    sys.setrecursionlimit(100)
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_initial_values, example_operations = parse(example_input)
    initial_values, operations = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_initial_values,
        example_operations,
        initial_values,
        operations,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_initial_values,
        example_operations,
        initial_values,
        operations,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
