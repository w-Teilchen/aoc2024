import pathlib
from typing import List

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 143
given_example_solution_of_second_part = 123


def parse(input: str, separator: str = " ") -> List[List[int]]:
    return [list(map(int, line.split(separator))) for line in input.strip().split("\n")]


def matches_rule(update: List[int], rule: List[int]) -> bool:
    if rule[0] not in update:
        return True
    if rule[1] not in update:
        return True
    return update.index(rule[0]) < update.index(rule[1])


def matches_all_rules(update: List[int], sorting_rules: List[List[int]]) -> bool:
    for rule in sorting_rules:
        if not matches_rule(update, rule):
            return False
    return True


def solve_first_part(updates: List[List[int]], sorting_rules: List[List[int]]) -> int:
    sum_of_middle_pages = 0
    for update in updates:
        if matches_all_rules(update, sorting_rules):
            if len(update) % 2 == 0:
                raise ValueError("The number of pages is even.")
            sum_of_middle_pages += update[len(update) // 2]
    return sum_of_middle_pages


def sort_update_according_to_rules(
    update: List[int], sorting_rules: List[List[int]]
) -> List[int]:
    while not matches_all_rules(update, sorting_rules):
        for rule in sorting_rules:
            if rule[0] in update and rule[1] in update:
                if update.index(rule[0]) > update.index(rule[1]):
                    index_0 = update.index(rule[0])
                    index_1 = update.index(rule[1])
                    update[index_0], update[index_1] = update[index_1], update[index_0]
    return update


def solve_second_part(updates: List[List[int]], sorting_rules: List[List[int]]) -> int:
    sum_of_middle_pages = 0
    for update in updates:
        if matches_all_rules(update, sorting_rules):
            continue
        reordered_update = sort_update_according_to_rules(update, sorting_rules)
        if len(reordered_update) % 2 == 0:
            raise ValueError("The number of pages is even.")
        sum_of_middle_pages += reordered_update[len(reordered_update) // 2]
    return sum_of_middle_pages


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
    example_numbers: List[List[int]],
    example_sorting_rules: List[List[int]],
    numbers: List[List[int]],
    sorting_rules: List[List[int]],
    solver: callable,
    given_solution: int,
):
    calculated_solution = solver(example_numbers, example_sorting_rules)
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(numbers, sorting_rules)
    print(f"The solution to the input is {calculated_solution}.")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    example_sorting_rules = read_input_from_file("example_sorting_rules.txt")
    input = read_input_from_file("input.txt")
    sorting_rules = read_input_from_file("sorting_rules.txt")
    if (
        example_input is None
        or input is None
        or example_sorting_rules is None
        or sorting_rules is None
    ):
        return
    example_numbers = parse(example_input, separator=",")
    example_sorting_rules = parse(example_sorting_rules, separator="|")
    numbers = parse(input, separator=",")
    sorting_rules = parse(sorting_rules, separator="|")

    print("\nSolving first part...")
    solve_part(
        example_numbers,
        example_sorting_rules,
        numbers,
        sorting_rules,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_numbers,
        example_sorting_rules,
        numbers,
        sorting_rules,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
