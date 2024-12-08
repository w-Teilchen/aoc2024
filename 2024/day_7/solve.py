import copy
import pathlib
from typing import List
import math

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 3749
given_example_solution_of_second_part = 11387


class CalibrationEquation:
    def __init__(self, input: str):
        self.test_value = int(input.split(":")[0].strip())
        self.numbers = list(map(int, input.split(":")[1].strip().split(" ")))
        self.operations = ["+"] * (len(self.numbers) - 1)

    def evaluate(self) -> int:
        result = self.numbers[0]
        for i in range(len(self.operations)):
            if self.operations[i] == "+":
                result += self.numbers[i + 1]
            elif self.operations[i] == "*":
                result *= self.numbers[i + 1]
            elif self.operations[i] == "||":
                result = int(str(result) + str(self.numbers[i + 1]))
        return result

    def permutate_multiplications_and_additions(self) -> bool:
        return permutate_two_operations(self.operations, "+", "*")

    def permutate_all_operations(self) -> bool:
        if not "||" in self.operations:
            if permutate_two_operations(self.operations, "+", "*"):
                return True
            for i in range(len(self.operations)):
                self.operations[i] = "+"
            self.operations[-1] = "||"
            return True

        operations_without_concatination = copy.deepcopy(self.operations)
        while "||" in operations_without_concatination:
            index = operations_without_concatination.index("||")
            operations_without_concatination = (
                operations_without_concatination[:index]
                + operations_without_concatination[index + 1 :]
            )
        if permutate_two_operations(operations_without_concatination, "+", "*"):
            index = 0
            for i in range(len(self.operations)):
                if not self.operations[i] == "||":
                    self.operations[i] = operations_without_concatination[index]
                    index += 1
            return True
        if "*" not in self.operations and "+" not in self.operations:
            return False
        for i in range(len(self.operations)):
            if not self.operations[i] == "||":
                self.operations[i] = "+"
        return permutate_two_operations(self.operations, "+", "||")


def permutate_two_operations(operations: List[str], a: str, b: str) -> bool:
    number_of_multiplications = operations.count(b)
    if number_of_multiplications == len(operations):
        return False
    if number_of_multiplications == 0:
        operations[-1] = b
        return True
    # Find the left-most multiplication and move it further to the left to create a new permutation.
    index = operations.index(b)
    if index != 0:
        operations[index - 1] = b
        operations[index] = a
        return True
    # In case the multiplication is at the beginning of the list, we need to find the next one.
    next_movable_index = find_next_movable_operation(operations[1:], b) + 1
    if (
        next_movable_index == -math.inf
    ):  # No multiplication could be moved, therefore a new multiplication needs to be introduced and all moved to the right.
        number_of_multiplications += 1
        for i in range(number_of_multiplications):
            operations[-1 - i] = b
        for i in range(len(operations) - number_of_multiplications):
            operations[i] = a
        return True
    number_of_multiplications_up_to_next_movable = operations[
        : next_movable_index + 1
    ].count(b)
    operations[next_movable_index] = a
    for i in range(number_of_multiplications_up_to_next_movable):
        operations[next_movable_index - i - 1] = b
    for i in range(next_movable_index - number_of_multiplications_up_to_next_movable):
        operations[i] = a
    return True


def find_next_movable_operation(operations: List[str], operation: str) -> int:
    if operation not in operations:
        return -math.inf
    index = operations.index(operation)
    if index != 0:
        return index
    return find_next_movable_operation(operations[1:], operation) + 1


def parse(input: str) -> List[CalibrationEquation]:
    return [CalibrationEquation(line) for line in input.strip().split("\n")]


def solve_first_part(calibration_equations: List[CalibrationEquation]) -> int:
    sum = 0
    for equation in calibration_equations:
        more_permutations = True
        while more_permutations:
            result = equation.evaluate()
            if result == equation.test_value:
                sum += result
                break
            more_permutations = equation.permutate_multiplications_and_additions()

    return sum


def solve_second_part(calibration_equations: List[CalibrationEquation]) -> int:
    sum = 0
    for equation in calibration_equations:
        more_permutations = True
        while more_permutations:
            result = equation.evaluate()
            if result == equation.test_value:
                sum += result
                break
            more_permutations = equation.permutate_all_operations()

    return sum


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
    example_calibration_equations = parse(example_input)
    calibration_equations = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_calibration_equations,
        calibration_equations,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_calibration_equations,
        calibration_equations,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
