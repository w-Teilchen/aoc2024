import pathlib
import re
from typing import List

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 161
given_example_solution_of_second_part = 48


def parse_input_with_do_and_dont_blocks(input: str) -> List[List[int]]:
    dont_position = re.search("don't", input)
    if dont_position is None:
        return parse(input)
    end_of_part_to_process = dont_position.regs[0][0]
    beginning_of_rest = dont_position.regs[0][1]
    part_to_process = input[:end_of_part_to_process]

    # Find next do and check that it is not a don't
    do_position = re.search("do", input[beginning_of_rest:])
    if do_position is None:  # No more do's
        return parse(part_to_process)
    dont_position = re.search("don't", input[beginning_of_rest:])
    if dont_position is not None and do_position.regs[0][0] == dont_position.regs[0][0]:
        return parse_input_with_do_and_dont_blocks(
            part_to_process + input[beginning_of_rest:][dont_position.regs[0][0] :]
        )

    unprocessed_end = input[beginning_of_rest:][do_position.regs[0][1] :]

    return parse_input_with_do_and_dont_blocks(part_to_process + unprocessed_end)


def parse(input: str) -> List[List[int]]:
    # Match the pattern mul(a, b) with the input
    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    matches = pattern.findall(input)
    numbers = [list(map(int, match)) for match in matches]
    return numbers


def solve_first_part(numbers: List[List[int]]) -> int:
    return sum([a * b for a, b in numbers])


def solve_second_part(numbers: List[List[int]]) -> int:
    return sum([a * b for a, b in numbers])


def read_input_from_file(path: str) -> str:
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
    example_numbers, numbers: List[List[int]], solver: callable, given_solution: int
):
    calculated_solution = solver(example_numbers)
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(numbers)
    print(f"The solution to the input is {calculated_solution}.")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    example_input_2 = read_input_from_file("example2.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return
    example_numbers = parse(example_input)
    numbers = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_numbers, numbers, solve_first_part, given_example_solution_of_first_part
    )

    print("\nSolving second part...")
    example_numbers = parse_input_with_do_and_dont_blocks(example_input_2)
    numbers = parse_input_with_do_and_dont_blocks(input)
    solve_part(
        example_numbers,
        numbers,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
