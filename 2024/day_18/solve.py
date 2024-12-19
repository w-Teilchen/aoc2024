import pathlib
from typing import List, Tuple
import sys
import time

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 22
given_example_solution_of_second_part = "6,1"


class MemorySpace:
    def __init__(self, corrupted_bytes: str, size: int, time: int):
        self.corrupted_bytes = corrupted_bytes
        self.memory_space = [["." for _ in range(size)] for _ in range(size)]
        for index, corrupted_byte in enumerate(corrupted_bytes.split("\n")):
            if index == time:
                break
            x, y = corrupted_byte.split(",")
            self.memory_space[int(y)][int(x)] = "#"
        self.start = (0, 0)
        self.end = (size - 1, size - 1)
        self.time = time
        self.minimal_paths = [
            [None for _ in range(len(self.memory_space[0]))]
            for _ in range(len(self.memory_space))
        ]

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.memory)


def parse(corrupted_bytes: str, size: int, time: int) -> MemorySpace:
    return MemorySpace(corrupted_bytes, size, time)


def get_direction(movement: str) -> tuple[int, int]:
    if movement == "^":
        return (0, -1)
    elif movement == "v":
        return (0, 1)
    elif movement == "<":
        return (-1, 0)
    elif movement == ">":
        return (1, 0)
    raise ValueError(f"Invalid movement: {movement}")


def move(memory: MemorySpace, position: Tuple[int, int], length: int = 0) -> None:
    for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        x = position[0] + direction[0]
        y = position[1] + direction[1]
        if (  # outside of the memory space
            x < 0
            or x >= len(memory.memory_space[0])
            or y < 0
            or y >= len(memory.memory_space)
        ):
            continue
        if memory.memory_space[y][x] == "#":  # corrupted byte
            continue
        if memory.minimal_paths[y][x] is None:  # first time visiting this cell
            memory.minimal_paths[y][x] = length + 1
        elif memory.minimal_paths[y][x] > length + 1:
            memory.minimal_paths[y][x] = length + 1
        elif memory.minimal_paths[y][x] <= length + 1:
            continue
        move(memory, (x, y), length + 1)


def solve_first_part(memory: MemorySpace) -> int:
    current_position = memory.start
    move(memory, current_position, 0)
    return memory.minimal_paths[memory.end[1]][memory.end[0]]


def solve_second_part(memory: MemorySpace) -> str:
    current_position = memory.start
    for time in range(memory.time, len(memory.corrupted_bytes)):
        memory.minimal_paths = [
            [None for _ in range(len(memory.memory_space[0]))]
            for _ in range(len(memory.memory_space))
        ]
        next_corrupted_byte = memory.corrupted_bytes.split("\n")[time].split(",")
        x, y = int(next_corrupted_byte[0]), int(next_corrupted_byte[1])
        memory.memory_space[y][x] = "#"
        move(memory, current_position, 0)
        if memory.minimal_paths[memory.end[1]][memory.end[0]] is None:
            return memory.corrupted_bytes.split("\n")[time]
    return None


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
    begin = time.time()
    calculated_solution = solver(example)
    print(f"{time.time()-begin} seconds needed to solve the example input.")
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    begin = time.time()
    calculated_solution = solver(input)
    print(f"{time.time()-begin} seconds needed to solve the actual input.")
    print(f"The solution to the input is {calculated_solution}")


def main():
    sys.setrecursionlimit(10000)

    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_memory = parse(example_input, 7, 12)
    memory = parse(input, 71, 1024)

    print("\nSolving first part...")
    solve_part(
        example_memory,
        memory,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_memory,
        memory,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
