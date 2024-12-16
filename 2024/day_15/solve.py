import pathlib
from typing import List, Tuple

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
given_example_solution_of_first_part = 10092
given_example_solution_of_second_part = 9021


class Warehouse:
    def __init__(self, warehouse: str):
        self.warehouse = list(list(row) for row in warehouse.split("\n"))
        self.robot_position = self.find_robot_position()

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.warehouse)

    def find_robot_position(self) -> Tuple[int, int]:
        for x, row in enumerate(self.warehouse):
            for y, cell in enumerate(row):
                if cell == "@":
                    return x, y
        raise ValueError("No robot found in the warehouse.")

    def move_box(self, position: Tuple[int, int], direction: str) -> bool:
        x, y = position
        dx, dy = translate_direction(direction)

        if self.warehouse[x + dx][y + dy] == ".":
            self.warehouse[x][y] = "."
            self.warehouse[x + dx][y + dy] = "O"
            return True
        if self.warehouse[x + dx][y + dy] == "#":
            return False
        if self.warehouse[x + dx][y + dy] == "O":
            if self.move_box((x + dx, y + dy), direction):
                self.warehouse[x][y] = "."
                self.warehouse[x + dx][y + dy] = "O"
                return True
            return False
        raise Exception(f"Invalid state reached.")

    def move_robot(self, direction: str) -> bool:
        x, y = self.robot_position
        dx, dy = translate_direction(direction)

        if self.warehouse[x + dx][y + dy] == "#":
            return False
        if self.warehouse[x + dx][y + dy] == ".":
            self.warehouse[x][y] = "."
            self.warehouse[x + dx][y + dy] = "@"
            self.robot_position = (x + dx, y + dy)
            return True
        if self.warehouse[x + dx][y + dy] == "O":
            if self.move_box((x + dx, y + dy), direction):
                self.warehouse[x][y] = "."
                self.warehouse[x + dx][y + dy] = "@"
                self.robot_position = (x + dx, y + dy)
                return True
            return False  # if the box could not be moved -> don't move the robot
        raise Exception(f"Invalid state reached.")

    def calculate_gps(self) -> int:
        gps = 0
        for y, row in enumerate(self.warehouse):
            for x, cell in enumerate(row):
                if cell == "O":
                    gps += x + 100 * y
        return gps


class WarehouseWithLargerBoxes(Warehouse):
    def __init__(self, warehouse: Warehouse):
        self.warehouse = []
        for row in warehouse.warehouse:
            self.warehouse.append([])
            for cell in row:
                if cell == "#":
                    self.warehouse[-1].extend(["#", "#"])
                elif cell == "O":
                    self.warehouse[-1].extend(["[", "]"])
                elif cell == ".":
                    self.warehouse[-1].extend([".", "."])
                elif cell == "@":
                    self.warehouse[-1].extend(["@", "."])
                else:
                    raise ValueError(f'Invalid tile "{cell}" in original warehouse.')
        self.robot_position = (
            warehouse.robot_position[0],
            2 * warehouse.robot_position[1],
        )

    def can_move_box(self, position: Tuple[int, int], direction: str) -> bool:
        x, y = position
        dx, dy = translate_direction(direction)
        if self.warehouse[x][y] != "[":
            raise ValueError(
                f"can_move_box should only be called on a box position ({self.warehouse[x][y]})."
            )

        if direction == "^" or direction == "v":
            if (
                self.warehouse[x + dx][y] == "."
                and self.warehouse[x + dx][y + 1] == "."
            ):
                return True
            if self.warehouse[x + dx][y] == "#" or self.warehouse[x + dx][y + 1] == "#":
                return False
            if self.warehouse[x + dx][y] == "[":
                return self.can_move_box((x + dx, y), direction)
            if (
                self.warehouse[x + dx][y] == "]"
                and self.warehouse[x + dx][y + 1] == "["
            ):
                return self.can_move_box(
                    (x + dx, y - 1), direction
                ) and self.can_move_box((x + dx, y + 1), direction)
            if self.warehouse[x + dx][y] == "]":
                return self.can_move_box((x + dx, y - 1), direction)
            if self.warehouse[x + dx][y + 1] == "[":
                return self.can_move_box((x + dx, y + 1), direction)
            raise Exception(f"Invalid state reached.")
        if direction == "<":
            if self.warehouse[x][y - 1] == ".":
                return True
            if self.warehouse[x][y - 1] == "#":
                return False
            if self.warehouse[x][y - 1] == "]":
                return self.can_move_box((x, y - 2), direction)
            raise Exception(f"Invalid state reached.")
        if direction == ">":
            if self.warehouse[x][y + 2] == ".":
                return True
            if self.warehouse[x][y + 2] == "#":
                return False
            if self.warehouse[x][y + 2] == "[":
                return self.can_move_box((x, y + 2), direction)
            raise Exception(f"Invalid state reached.")
        raise Exception(f"Invalid state reached.")

    def move_box(self, position: Tuple[int, int], direction: str) -> None:
        x, y = position
        dx, dy = translate_direction(direction)

        if self.warehouse[x][y] != "[":
            raise ValueError(
                f"move_box should only be called on a box position ({self.warehouse[x][y]})."
            )

        if direction == "^" or direction == "v":
            if self.warehouse[x + dx][y] == "#" or self.warehouse[x + dx][y + 1] == "#":
                raise ValueError("Box could not be moved.")
            if self.warehouse[x + dx][y] == "[":
                self.move_box((x + dx, y), direction)
            if self.warehouse[x + dx][y] == "]":
                self.move_box((x + dx, y - 1), direction)
            if self.warehouse[x + dx][y + 1] == "[":
                self.move_box((x + dx, y + 1), direction)
            self.warehouse[x][y] = "."
            self.warehouse[x][y + 1] = "."
            self.warehouse[x + dx][y] = "["
            self.warehouse[x + dx][y + 1] = "]"
            return

        if direction == "<":
            if self.warehouse[x][y - 1] == "#":
                raise ValueError("Box could not be moved.")
            if self.warehouse[x][y - 1] == "]":
                self.move_box((x, y - 2), direction)
            self.warehouse[x][y - 1] = "["
            self.warehouse[x][y] = "]"
            self.warehouse[x][y + 1] = "."
            return

        if direction == ">":
            if self.warehouse[x][y + 2] == "#":
                raise ValueError("Box could not be moved.")
            if self.warehouse[x][y + 2] == "[":
                self.move_box((x, y + 2), direction)
            self.warehouse[x][y] = "."
            self.warehouse[x][y + 1] = "["
            self.warehouse[x][y + 2] = "]"
            return

        raise Exception(f"Invalid state reached.")

    def move_robot(self, direction: str) -> None:
        x, y = self.robot_position
        dx, dy = translate_direction(direction)

        if self.warehouse[x + dx][y + dy] == "#":
            return
        if self.warehouse[x + dx][y + dy] == ".":
            self.warehouse[x][y] = "."
            self.warehouse[x + dx][y + dy] = "@"
            self.robot_position = (x + dx, y + dy)
            return
        if self.warehouse[x + dx][y + dy] == "[":
            if self.can_move_box((x + dx, y + dy), direction):
                self.move_box((x + dx, y + dy), direction)
                self.warehouse[x][y] = "."
                self.warehouse[x + dx][y + dy] = "@"
                self.robot_position = (x + dx, y + dy)
            return
        if self.warehouse[x + dx][y + dy] == "]":
            if self.can_move_box((x + dx, y - 1 + dy), direction):
                self.move_box((x + dx, y - 1 + dy), direction)
                self.warehouse[x][y] = "."
                self.warehouse[x + dx][y + dy] = "@"
                self.robot_position = (x + dx, y + dy)
            return
        raise Exception(f"Invalid state reached.")

    def calculate_gps(self) -> int:
        gps = 0
        for y, row in enumerate(self.warehouse):
            for x, cell in enumerate(row):
                if cell == "[":
                    gps += x + 100 * y
        return gps


def translate_direction(direction: str) -> Tuple[int, int]:
    if direction == "^":
        return -1, 0
    if direction == "v":
        return 1, 0
    if direction == "<":
        return 0, -1
    if direction == ">":
        return 0, 1
    raise ValueError(f"Invalid direction {direction}.")


def parse_warehouse(input: str) -> Warehouse:
    return Warehouse(input)


def parse(input: str) -> Tuple[Warehouse, str]:
    warehouse_input, move_input = input.split("\n\n")
    return parse_warehouse(warehouse_input), move_input.replace("\n", "").strip()


def solve_first_part(warehouse: Warehouse, move_sequence: List[str]) -> int:
    for move in move_sequence:
        warehouse.move_robot(move)

    print(warehouse)
    return warehouse.calculate_gps()


def solve_second_part(
    warehouse: WarehouseWithLargerBoxes, move_sequence: List[str]
) -> int:
    print(warehouse)
    for move in move_sequence:
        warehouse.move_robot(move)

    print(warehouse)
    return warehouse.calculate_gps()


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


def solve_part(
    example_warehouse,
    example_move_sequence,
    warehouse,
    move_sequence,
    solver: callable,
    given_solution: int,
) -> None:
    """Solves part of the puzzle after checking the solver using the example solution.

    Args:
        example: The example input used for checking.
        input: The actual input required for the current puzzle.
        solver: The function to solve the part of the puzzle.
        given_solution: The expected solution for the example input.
    """
    calculated_solution = solver(example_warehouse, example_move_sequence)
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(warehouse, move_sequence)
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_warehouse, example_move_sequence = parse(example_input)
    warehouse, move_sequence = parse(input)

    example_warehouse_with_larger_boxes = WarehouseWithLargerBoxes(example_warehouse)
    warehouse_with_larger_boxes = WarehouseWithLargerBoxes(warehouse)

    print("\nSolving first part...")
    solve_part(
        example_warehouse,
        example_move_sequence,
        warehouse,
        move_sequence,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_warehouse_with_larger_boxes,
        example_move_sequence,
        warehouse_with_larger_boxes,
        move_sequence,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
