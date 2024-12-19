import pathlib
from typing import List, Tuple
import copy
import time

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 6
given_example_solution_of_second_part = 16


def parse(input: str) -> Tuple[List[str], List[str]]:
    towel_designs = input.split("\n\n")[0].split(", ")
    desired_designs = input.split("\n\n")[1].strip().split("\n")
    return towel_designs, desired_designs


def match_design(
    towel_designs: List[str], desired_design: str, current_position: int
) -> bool:
    if current_position == len(desired_design):
        return True
    for towel_design in towel_designs:
        if desired_design.startswith(towel_design, current_position):
            if match_design(
                towel_designs, desired_design, current_position + len(towel_design)
            ):
                return True
    return False


def remove_unnecessary_designs(towel_designs: List[str]) -> None:
    towel_designs.sort(key=lambda x: len(x), reverse=True)
    index = 0
    while index < len(towel_designs):
        if match_design(
            towel_designs[:index] + towel_designs[index + 1 :], towel_designs[index], 0
        ):
            towel_designs.pop(index)
        else:
            index += 1


def solve_first_part(towel_designs: List[str], desired_designs: List[str]) -> int:
    count = 0
    begin = time.time()
    remove_unnecessary_designs(towel_designs)
    for index, design in enumerate(desired_designs):
        if index % 100 == 0 and index != 0:
            print(f"{index} designs checked in {time.time()-begin:.4f} seconds.")
        if match_design(towel_designs, design, 0):
            count += 1
    return count


def sort_towel_designs_into_dict(
    unprocessed_towel_designs: List[str],
) -> dict[List[str]]:
    towel_designs = {}
    for towel in unprocessed_towel_designs:
        if towel[0] not in towel_designs:
            towel_designs[towel[0]] = [towel]
        else:
            towel_designs[towel[0]].append(towel)
    return towel_designs


def count_matching_designs(
    towel_designs: dict[str, List[str]],
    desired_design: str,
    current_position: int,
    memory: dict = None,
) -> int:
    if current_position == len(desired_design):
        return 1
    if memory is None:
        memory = {}
    if current_position in memory:
        return memory[current_position]
    count = 0
    if desired_design[current_position] in towel_designs:
        for towel_design in towel_designs[desired_design[current_position]]:
            if desired_design.startswith(towel_design, current_position):
                count += count_matching_designs(
                    towel_designs,
                    desired_design,
                    current_position + len(towel_design),
                    memory,
                )
    memory[current_position] = count
    return count


def solve_second_part(towel_designs: List[str], desired_designs: List[str]) -> int:
    towel_designs.sort(key=lambda x: len(x), reverse=True)
    count = 0
    begin = time.time()
    minimal_towel_designs = copy.deepcopy(towel_designs)
    remove_unnecessary_designs(minimal_towel_designs)
    towel_designs = sort_towel_designs_into_dict(towel_designs)
    for index, design in enumerate(desired_designs):
        if index % 100 == 0 and index != 0:
            print(f"{index} designs checked in {time.time()-begin:.4f} seconds.")
        if match_design(minimal_towel_designs, design, 0):
            count += count_matching_designs(towel_designs, design, 0)
    return count


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
    example_towel_designs,
    example_desired_designs,
    towel_designs,
    desired_designs,
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
    begin = time.time()
    calculated_solution = solver(
        copy.deepcopy(example_towel_designs), copy.deepcopy(example_desired_designs)
    )
    print(f"{time.time()-begin:.4f} seconds needed to solve the example input.")
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    begin = time.time()
    calculated_solution = solver(
        copy.deepcopy(towel_designs), copy.deepcopy(desired_designs)
    )
    print(f"{time.time()-begin:.4f} seconds needed to solve the actual input.")
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_towel_designs, example_desired_designs = parse(example_input)
    towel_designs, desired_designs = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_towel_designs,
        example_desired_designs,
        towel_designs,
        desired_designs,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_towel_designs,
        example_desired_designs,
        towel_designs,
        desired_designs,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
