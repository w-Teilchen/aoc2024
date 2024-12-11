import pathlib
from typing import List
import time

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 55312
given_example_solution_of_second_part = 65601038650482

twenty_five_blink_lookup_table = {}


def parse(input: str, separator: str = " ") -> List[List[int]]:
    return list(map(int, input.split(separator)))


def blink(number: int) -> List[int]:
    if number == 0:
        return [1]
    number_of_digits = len(str(number))
    if number_of_digits % 2 == 0:
        first_half_of_digits = number // 10 ** (number_of_digits // 2)
        second_half_of_digits = number % 10 ** (number_of_digits // 2)
        return [first_half_of_digits, second_half_of_digits]
    return [number * 2024]


def blink_multiple_times(numbers: List[int], remaining_blinks: int) -> List[int]:
    if remaining_blinks == 0:
        return numbers
    new_numbers = []
    for number in numbers:
        new_numbers.extend(blink(number))
    return blink_multiple_times(new_numbers, remaining_blinks - 1)


def blink_twentyfive_times(number: int) -> List[int]:
    if number in twenty_five_blink_lookup_table:
        return twenty_five_blink_lookup_table[number]

    stones_after_twentyfive_blinks = blink_multiple_times([number], 25)
    twenty_five_blink_lookup_table[number] = stones_after_twentyfive_blinks
    return stones_after_twentyfive_blinks


def count_stones_after_seventyfive_blinks(number: int) -> List[int]:
    number_of_stones = 0
    for stone in blink_twentyfive_times(number):
        stones_after_fifty_blinks = blink_twentyfive_times(stone)
        for stone in stones_after_fifty_blinks:
            number_of_stones += len(blink_twentyfive_times(stone))

    return number_of_stones


def solve_first_part(numbers: List[List[int]]) -> int:
    start = time.time()
    number_of_stones = 0
    for number in numbers:
        number_of_stones += len(blink_twentyfive_times(number))
    print(f"Execution time: {time.time() - start}")

    return number_of_stones


def solve_second_part(numbers: List[List[int]]) -> int:
    start = time.time()
    number_of_stones = 0
    for number in numbers:
        number_of_stones += count_stones_after_seventyfive_blinks(number)
    print(f"Execution time: {time.time() - start}")

    return number_of_stones


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
    numbers = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_numbers, numbers, solve_first_part, given_example_solution_of_first_part
    )

    print("\nSolving second part...")
    solve_part(
        example_numbers,
        numbers,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
