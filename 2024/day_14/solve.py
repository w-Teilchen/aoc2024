import pathlib
from typing import List
import copy
import numpy as np
import re

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 12
given_example_solution_of_second_part = 0


class Robot:
    def __init__(self, position: List[int], velocity: List[int]):
        self.position = np.array(position)
        self.velocity = np.array(velocity)

    def move(self):
        self.position += self.velocity

    def get_quadrant(self, quadrant_size: np.array) -> int:
        position_within_space = self.position % (2 * quadrant_size + 1)
        if (
            position_within_space[0] < quadrant_size[0]
            and position_within_space[1] < quadrant_size[1]
        ):
            return 1
        if (
            position_within_space[0] < quadrant_size[0]
            and position_within_space[1] > quadrant_size[1]
        ):
            return 2
        if (
            position_within_space[0] > quadrant_size[0]
            and position_within_space[1] < quadrant_size[1]
        ):
            return 3
        if (
            position_within_space[0] > quadrant_size[0]
            and position_within_space[1] > quadrant_size[1]
        ):
            return 4
        return 0  # The robot is on the border of the quadrants.

    def get_grid_position(self, quadrant_size: np.array, grid: np.array) -> np.array:
        space_size = 2 * quadrant_size + 1
        position_within_space = self.position % space_size
        return (position_within_space / space_size * grid.shape).astype(int)

    def __str__(self):
        return f"Position: {self.position}, Velocity: {self.velocity}"


def parse(input: str):
    robots = []
    for line in input.splitlines():
        numbers = list(map(int, re.findall(r"-?\d+", line)))
        robots.append(Robot(numbers[:2], numbers[2:]))
    return robots


def solve_first_part(robots: List[Robot], quadrant_size: np.array) -> int:
    for time in range(100):
        for robot in robots:
            robot.move()
    robots_in_quadrants = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for robot in robots:
        robots_in_quadrants[robot.get_quadrant(quadrant_size)] += 1
    return (
        robots_in_quadrants[1]
        * robots_in_quadrants[2]
        * robots_in_quadrants[3]
        * robots_in_quadrants[4]
    )


def display_space(robots: List[Robot], quadrant_size: np.array) -> None:
    for y in range(2 * quadrant_size[1] + 1):
        for x in range(2 * quadrant_size[0] + 1):
            if any(
                [
                    robot.position[0] % (2 * quadrant_size[0] + 1) == x
                    and robot.position[1] % (2 * quadrant_size[1] + 1) == y
                    for robot in robots
                ]
            ):
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def calculate_entropy(robots_in_grid: np.array) -> float:
    total_robots = np.sum(robots_in_grid)
    entropy = 0
    for i in range(robots_in_grid.shape[0]):
        for j in range(robots_in_grid.shape[1]):
            if robots_in_grid[i, j] > 0:
                probability = robots_in_grid[i, j] / total_robots
                entropy -= probability * np.log2(probability)
    return entropy


def solve_second_part(robots: List[Robot], quadrant_size: np.array) -> int:
    time_with_lowest_entropy = 0
    lowest_entropy = float("inf")
    robots_with_lowest_entropy = None
    for time in range(1, 10000):
        robots_in_grid = np.zeros((9, 9), dtype=int)
        for robot in robots:
            robot.move()
            grid_position = robot.get_grid_position(quadrant_size, robots_in_grid)
            robots_in_grid[grid_position[1], grid_position[0]] += 1

        entropy = calculate_entropy(robots_in_grid)
        if entropy < lowest_entropy:
            lowest_entropy = entropy
            time_with_lowest_entropy = time
            robots_with_lowest_entropy = copy.deepcopy(robots)

    display_space(robots_with_lowest_entropy, quadrant_size)
    return time_with_lowest_entropy


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
    if (
        solver == solve_first_part
    ):  # Only the first part of the puzzle has a given solution.
        calculated_solution = solver(example, np.array([5, 3]))
        assert (
            calculated_solution == given_solution
        ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
        print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(input, np.array([50, 51]))
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_robots = parse(example_input)
    unmoved_robots = parse(input)
    print("\nSolving first part...")

    robots = copy.deepcopy(unmoved_robots)
    solve_part(
        example_robots,
        robots,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    robots = copy.deepcopy(unmoved_robots)
    solve_part(
        example_robots,
        robots,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
