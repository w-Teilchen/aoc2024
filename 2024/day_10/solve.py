import pathlib
from typing import List, Set, Tuple

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 36
given_example_solution_of_second_part = 81


def parse(input: str, separator: str = " ") -> List[List[int]]:
    return [list(map(int, line)) for line in input.strip().split("\n")]


def evaluate_trail(map: List[List[int]], x: int, y: int, previous_height=-1):
    if x < 0 or y < 0 or x >= len(map) or y >= len(map[0]):
        return {None}

    current_height = map[x][y]
    if previous_height == 8 and current_height == 9:
        return {(x, y)}
    if current_height == previous_height + 1:
        return (
            evaluate_trail(map, x - 1, y, current_height)
            .union(evaluate_trail(map, x + 1, y, current_height))
            .union(evaluate_trail(map, x, y - 1, current_height))
            .union(evaluate_trail(map, x, y + 1, current_height))
        )

    return {None}


def count_individual_trails(
    map: List[List[int]], x: int, y: int, previous_height=-1
) -> int:
    if x < 0 or y < 0 or x >= len(map) or y >= len(map[0]):
        return 0

    current_height = map[x][y]
    if previous_height == 8 and current_height == 9:
        return 1
    if current_height == previous_height + 1:
        return (
            count_individual_trails(map, x - 1, y, current_height)
            + count_individual_trails(map, x + 1, y, current_height)
            + count_individual_trails(map, x, y - 1, current_height)
            + count_individual_trails(map, x, y + 1, current_height)
        )

    return 0


def solve_first_part(map: List[List[int]]) -> int:
    sum_of_trail_scores = 0
    for x, line in enumerate(map):
        for y, value in enumerate(line):
            if value == 0:
                reachable_peaks = {
                    peak for peak in evaluate_trail(map, x, y) if peak is not None
                }
                sum_of_trail_scores += len(reachable_peaks)
    return sum_of_trail_scores


def solve_second_part(map: List[List[int]]) -> int:
    sum_of_trail_scores = 0
    for x, line in enumerate(map):
        for y, value in enumerate(line):
            if value == 0:
                sum_of_trail_scores += count_individual_trails(map, x, y)
    return sum_of_trail_scores


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
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return
    example_numbers = parse(example_input)
    map = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_numbers, map, solve_first_part, given_example_solution_of_first_part
    )

    print("\nSolving second part...")
    solve_part(
        example_numbers,
        map,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
