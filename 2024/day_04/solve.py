import pathlib
from typing import List

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 18
given_example_solution_of_second_part = 9


def parse(input: str) -> List[List[str]]:
    return [list(line) for line in input.split("\n")]


def count_horizontal_xmas(matrix: List[List[str]]) -> int:
    counter = 0
    for row in matrix:
        for i in range(len(row) - 3):
            if (
                row[i] == "X"
                and row[i + 1] == "M"
                and row[i + 2] == "A"
                and row[i + 3] == "S"
            ):
                counter += 1
            if (
                row[i + 3] == "X"
                and row[i + 2] == "M"
                and row[i + 1] == "A"
                and row[i] == "S"
            ):
                counter += 1
    return counter


def count_vertical_xmas(matrix: List[List[str]]) -> int:
    counter = 0
    for i in range(len(matrix) - 3):
        for j in range(len(matrix[i])):
            if (
                matrix[i][j] == "X"
                and matrix[i + 1][j] == "M"
                and matrix[i + 2][j] == "A"
                and matrix[i + 3][j] == "S"
            ):
                counter += 1
            if (
                matrix[i + 3][j] == "X"
                and matrix[i + 2][j] == "M"
                and matrix[i + 1][j] == "A"
                and matrix[i][j] == "S"
            ):
                counter += 1
    return counter


def count_diagonal_xmas(matrix: List[List[str]]) -> int:
    counter = 0
    for i in range(len(matrix) - 3):
        for j in range(len(matrix[i]) - 3):
            if (
                matrix[i][j] == "X"
                and matrix[i + 1][j + 1] == "M"
                and matrix[i + 2][j + 2] == "A"
                and matrix[i + 3][j + 3] == "S"
            ):
                counter += 1
            if (
                matrix[i + 3][j + 3] == "X"
                and matrix[i + 2][j + 2] == "M"
                and matrix[i + 1][j + 1] == "A"
                and matrix[i][j] == "S"
            ):
                counter += 1
    for i in range(len(matrix) - 3):
        for j in range(3, len(matrix[i])):
            if (
                matrix[i][j] == "X"
                and matrix[i + 1][j - 1] == "M"
                and matrix[i + 2][j - 2] == "A"
                and matrix[i + 3][j - 3] == "S"
            ):
                counter += 1
            if (
                matrix[i + 3][j - 3] == "X"
                and matrix[i + 2][j - 2] == "M"
                and matrix[i + 1][j - 1] == "A"
                and matrix[i][j] == "S"
            ):
                counter += 1
    return counter


def solve_first_part(matrix: List[List[str]]) -> int:
    return (
        count_horizontal_xmas(matrix)
        + count_vertical_xmas(matrix)
        + count_diagonal_xmas(matrix)
    )


def solve_second_part(matrix: List[List[str]]) -> int:
    count = 0
    for i in range(len(matrix) - 2):
        for j in range(len(matrix[i]) - 2):
            if (
                matrix[i + 1][j + 1] == "A"
                and (
                    (matrix[i][j] == "M" and matrix[i + 2][j + 2] == "S")
                    or (matrix[i][j] == "S" and matrix[i + 2][j + 2] == "M")
                )
                and (
                    (matrix[i][j + 2] == "M" and matrix[i + 2][j] == "S")
                    or (matrix[i][j + 2] == "S" and matrix[i + 2][j] == "M")
                )
            ):
                count += 1
    return count


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
    test = list("foobar")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return
    example_matrix = parse(example_input)
    matrix = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_matrix, matrix, solve_first_part, given_example_solution_of_first_part
    )

    print("\nSolving second part...")
    solve_part(
        example_matrix,
        matrix,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
