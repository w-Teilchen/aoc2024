import pathlib
from typing import List, Tuple
import sys
import time

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 0
given_example_solution_of_second_part = 0


class RaceTrack:
    def __init__(self, input: str):
        self.track = list(list(line) for line in input.strip().split("\n"))
        self.start = self.find_start()
        self.end = self.find_end()
        self.distance_to_start = [
            [None for _ in range(len(self.track[0]))] for _ in range(len(self.track))
        ]
        self.distance_to_start[self.start[1]][self.start[0]] = 0

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.track)

    def find_start(self) -> tuple[int, int]:
        for y, line in enumerate(self.track):
            for x, cell in enumerate(line):
                if cell == "S":
                    return (x, y)
        raise ValueError("No start found in race track.")

    def find_end(self) -> tuple[int, int]:
        for y, line in enumerate(self.track):
            for x, cell in enumerate(line):
                if cell == "E":
                    return (x, y)
        raise ValueError("No end found in race track.")

    def mark_shortest_path(self) -> None:
        x, y = self.end
        self.track[y][x] = self.distance_to_start[y][x]
        while (x, y) != self.start:
            for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                x_prev = x + direction[0]
                y_prev = y + direction[1]
                if (
                    self.distance_to_start[y_prev][x_prev]
                    == self.distance_to_start[y][x] - 1
                ):
                    self.track[y][x] = str(self.distance_to_start[y][x])
                    x, y = x_prev, y_prev
                    break
        self.track[y][x] = "0"


def parse(input: str) -> RaceTrack:
    return RaceTrack(input)


def move(race_track: RaceTrack, position: Tuple[int, int], length: int = 0) -> None:
    for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        x = position[0] + direction[0]
        y = position[1] + direction[1]
        if race_track.track[y][x] == "#":  # wall
            continue
        if race_track.distance_to_start[y][x] is None:  # first time visiting this cell
            race_track.distance_to_start[y][x] = length + 1
        elif race_track.distance_to_start[y][x] > length + 1:
            race_track.distance_to_start[y][x] = length + 1
        elif race_track.distance_to_start[y][x] <= length + 1:
            continue
        move(race_track, (x, y), length + 1)


def solve_first_part(race_track: RaceTrack) -> int:
    current_position = race_track.start
    move(race_track, current_position, 0)
    race_track.mark_shortest_path()
    possible_cheats = []
    for y, line in enumerate(race_track.track):
        for x, cell in enumerate(line):
            if not cell.isdigit():
                continue
            for direction in [
                (0, -2),
                (0, 2),
                (-2, 0),
                (2, 0),
                (-1, -1),
                (-1, 1),
                (1, 1),
                (1, -1),
            ]:
                x_cheat = x + direction[0]
                y_cheat = y + direction[1]
                if (
                    x_cheat < 0
                    or x_cheat >= len(race_track.track[0])
                    or y_cheat < 0
                    or y_cheat >= len(race_track.track)
                ):
                    continue
                if not race_track.track[y_cheat][x_cheat].isdigit():
                    continue
                shortcut = int(race_track.track[y_cheat][x_cheat]) - int(cell) - 2
                if (shortcut) > 0:
                    possible_cheats.append(shortcut)
    possible_cheats.sort()
    return len([cheat for cheat in possible_cheats if cheat >= 100])


def solve_second_part(race_track: RaceTrack) -> int:
    # It is assumed that the first part of the puzzle is solved before this part.
    possible_cheats = []
    for y, line in enumerate(race_track.track):
        for x, cell in enumerate(line):
            if not cell.isdigit():
                continue
            for x_direction in range(-20, 21):
                rest = 20 - abs(x_direction)
                for y_direction in range(-rest, rest + 1):
                    x_cheat = x + x_direction
                    y_cheat = y + y_direction
                    if (
                        x_cheat < 0
                        or x_cheat >= len(race_track.track[0])
                        or y_cheat < 0
                        or y_cheat >= len(race_track.track)
                    ):
                        continue
                    if not race_track.track[y_cheat][x_cheat].isdigit():
                        continue
                    shortcut = (
                        int(race_track.track[y_cheat][x_cheat])
                        - int(cell)
                        - abs(y_direction)
                        - abs(x_direction)
                    )
                    if (shortcut) > 0:
                        possible_cheats.append(shortcut)
    possible_cheats.sort(reverse=True)
    return len([cheat for cheat in possible_cheats if cheat >= 100])


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

    example_race_track = parse(example_input)
    race_track = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_race_track,
        race_track,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_race_track,
        race_track,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
