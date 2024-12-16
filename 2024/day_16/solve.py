import pathlib
from typing import List
import copy
import sys

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 7036
given_example_solution_of_second_part = 45


class Maze:
    def __init__(self, maze: str):
        self.maze = list(list(line) for line in maze.strip().split("\n"))
        self.start = self.find_start()
        self.end = self.find_end()
        self.minimal_paths = [
            [None for _ in range(len(self.maze[0]))] for _ in range(len(self.maze))
        ]

    def find_start(self) -> tuple[int, int]:
        for y, line in enumerate(self.maze):
            for x, cell in enumerate(line):
                if cell == "S":
                    return (x, y)
        raise ValueError("No start found in maze.")

    def find_end(self) -> tuple[int, int]:
        for y, line in enumerate(self.maze):
            for x, cell in enumerate(line):
                if cell == "E":
                    return (x, y)
        raise ValueError("No end found in maze.")

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.maze)


class Path:
    def __init__(self, movements: List[str], x: int, y: int, length: int):
        self.movements = movements
        self.x = x
        self.y = y
        self.length = length

    def extend(self, movement: str, maze) -> bool:
        x, y = self.x, self.y
        if movement == "^":
            y -= 1
        elif movement == "v":
            y += 1
        elif movement == "<":
            x -= 1
        elif movement == ">":
            x += 1

        if maze.maze[y][x] == "#":
            return False

        self.x, self.y = x, y
        last_movement = self.movements[-1]
        self.movements.append(movement)
        if last_movement == movement:
            self.length += 1
        else:
            self.length += 1001

        if (  # Exclude paths that are already longer than the shortest path.
            maze.minimal_paths[maze.end[1]][maze.end[0]] is not None
            and maze.minimal_paths[maze.end[1]][maze.end[0]][0].length < self.length
        ):
            return False

        if maze.minimal_paths[y][x] is None:
            maze.minimal_paths[y][x] = [self]
            return True
        minimal_path_length = min(path.length for path in maze.minimal_paths[y][x])
        if (
            minimal_path_length + 1000 < self.length
        ):  # If the new path is more than 1000 steps longer than the shortest path, it can be excluded (better orientation doesn't suffice).
            return False
        for path in maze.minimal_paths[y][x]:
            if path.movements[-1] == movement:
                if path.length < self.length:
                    return False
                if path.length > self.length:
                    maze.minimal_paths[y][x].remove(path)
            else:
                if path.length > self.length + 1000:
                    maze.minimal_paths[y][x].remove(path)
        maze.minimal_paths[y][x].append(self)
        return True


def parse(input: str) -> Maze:
    return Maze(input)


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


def move(maze: Maze, path: Path) -> Path:
    for movement in ["^", "v", "<", ">"]:
        direction = get_direction(movement)
        x, y = path.x + direction[0], path.y + direction[1]
        if x < 0 or x >= len(maze.maze[0]) or y < 0 or y >= len(maze.maze):
            continue
        new_path = copy.deepcopy(path)
        if new_path.extend(movement, maze):
            move(maze, new_path)


def solve_first_part(maze: Maze) -> int:
    current_position = maze.start
    move(maze, Path([">"], current_position[0], current_position[1], 0))
    return maze.minimal_paths[maze.end[1]][maze.end[0]][0].length


def solve_second_part(maze: Maze) -> int:
    paths_to_end = maze.minimal_paths[maze.end[1]][maze.end[0]]
    print(f"Found {len(paths_to_end)} optimal paths to the end.")
    maze.maze[maze.start[1]][maze.start[0]] = "O"
    for path in paths_to_end:
        movements = path.movements[1:]
        x, y = maze.start
        for move in movements:
            direction = get_direction(move)
            x += direction[0]
            y += direction[1]
            maze.maze[y][x] = "O"

    print(maze)
    return sum(line.count("O") for line in maze.maze)


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
    calculated_solution = solver(example)
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(input)
    print(f"The solution to the input is {calculated_solution}")


def main():
    sys.setrecursionlimit(10000)

    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    parsed_example = parse(example_input)
    parsed_input = parse(input)

    print("\nSolving first part...")
    solve_part(
        parsed_example,
        parsed_input,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        parsed_example,
        parsed_input,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
