import copy
import pathlib
from typing import List
from enum import Enum

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 41
given_example_solution_of_second_part = 6


def parse(input: str, separator: str = " ") -> List[List[int]]:
    return [list(line) for line in input.strip().split("\n")]


def check_if_guard_needs_to_turn(tile_in_walking_direction: str) -> bool:
    return tile_in_walking_direction == "#" or tile_in_walking_direction == "O"


def turn_guard(
    area: List[List[str]], guard_position: List[int], guard_direction: List[int]
) -> None:
    guard_state = area[guard_position[0]][guard_position[1]]
    if guard_state == "^":
        guard_state = ">"
    elif guard_state == ">":
        guard_state = "v"
    elif guard_state == "v":
        guard_state = "<"
    elif guard_state == "<":
        guard_state = "^"
    else:
        raise ValueError(f"Invalid guard state: {guard_state}")
    area[guard_position[0]][guard_position[1]] = guard_state
    guard_direction[0], guard_direction[1] = get_direction_of_guard(guard_state)


class State(Enum):
    IN_AREA = 1
    LEFT_AREA = 2
    IN_LOOP = 3


def update_position_of_guard(
    area: List[List[str]],
    guard_position: List[int],
    guard_direction: List[int],
) -> State:
    guard_state = area[guard_position[0]][guard_position[1]]
    new_i = guard_position[0] + guard_direction[0]
    new_j = guard_position[1] + guard_direction[1]
    if (
        new_i < 0
        or new_i >= len(area)
        or new_j < 0
        or new_j >= len(area[guard_position[0]])
    ):
        return State.LEFT_AREA
    if area[new_i][new_j] == guard_state:
        return State.IN_LOOP
    if not check_if_guard_needs_to_turn(area[new_i][new_j]):
        guard_position[0] = new_i
        guard_position[1] = new_j
        area[new_i][new_j] = guard_state
        return State.IN_AREA
    turn_guard(area, guard_position, guard_direction)
    return State.IN_AREA


def count_number_of_visited_tiles(area: List[List[str]]) -> int:
    return sum(
        [
            row.count("^") + row.count("v") + row.count("<") + row.count(">")
            for row in area
        ]
    )


def tile_contains_guard(tile: str) -> bool:
    return tile in ["^", "v", "<", ">"]


def get_guard_position(area: List[List[str]]) -> List[int]:
    for i, row in enumerate(area):
        for j, tile in enumerate(row):
            if tile_contains_guard(tile):
                return [i, j]
    raise ValueError("No guard found in the area.")


def get_direction_of_guard(guard_state: str) -> List[int]:
    if guard_state == "^":
        return [-1, 0]
    elif guard_state == "v":
        return [1, 0]
    elif guard_state == "<":
        return [0, -1]
    elif guard_state == ">":
        return [0, 1]
    raise ValueError(f"Invalid guard state: {guard_state}")


def solve_first_part(original_area: List[List[str]]) -> int:
    area = copy.deepcopy(original_area)
    guard_position = get_guard_position(area)
    guard_direction = get_direction_of_guard(area[guard_position[0]][guard_position[1]])
    guard_in_area = State.IN_AREA
    while guard_in_area == State.IN_AREA:
        guard_in_area = update_position_of_guard(area, guard_position, guard_direction)

    return count_number_of_visited_tiles(area)


def get_tiles_on_the_guards_path(original_area: List[List[str]]) -> List[List[str]]:
    area = copy.deepcopy(original_area)
    guard_position = get_guard_position(area)
    guard_direction = get_direction_of_guard(area[guard_position[0]][guard_position[1]])
    guard_in_area = State.IN_AREA
    while guard_in_area == State.IN_AREA:
        guard_in_area = update_position_of_guard(area, guard_position, guard_direction)
    # return list with all tiles the contain <, >, ^, v
    return [
        [i, j]
        for i, row in enumerate(area)
        for j, tile in enumerate(row)
        if tile_contains_guard(tile)
    ]


def is_tile_empty(tile: str) -> bool:
    return tile == "."


def solve_second_part(original_area: List[List[str]]) -> int:
    size_of_area = len(original_area) * len(original_area[0])
    original_guard_position = get_guard_position(original_area)
    original_guard_orientation = get_direction_of_guard(
        original_area[original_guard_position[0]][original_guard_position[1]]
    )

    tiles_on_the_guards_path = get_tiles_on_the_guards_path(original_area)
    number_of_positions_that_lead_to_loop = 0
    for position in tiles_on_the_guards_path:
        if not is_tile_empty(original_area[position[0]][position[1]]):
            continue
        area = copy.deepcopy(original_area)
        area[position[0]][position[1]] = "O"
        guard_position = copy.deepcopy(original_guard_position)
        guard_direction = copy.deepcopy(original_guard_orientation)
        guard_in_area = State.IN_AREA
        for step in range(size_of_area):
            guard_in_area = update_position_of_guard(
                area, guard_position, guard_direction
            )
            if guard_in_area == State.LEFT_AREA or guard_in_area == State.IN_LOOP:
                break
        if guard_in_area == State.IN_LOOP or step == size_of_area - 1:
            number_of_positions_that_lead_to_loop += 1

    return number_of_positions_that_lead_to_loop


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
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return
    example_area = parse(example_input)
    area = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_area, area, solve_first_part, given_example_solution_of_first_part
    )

    print("\nSolving second part...")
    solve_part(
        example_area,
        area,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
