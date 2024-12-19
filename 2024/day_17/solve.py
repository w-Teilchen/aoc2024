import pathlib
from typing import List
import copy
import time

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
example_file = "example.txt"
given_example_solution_of_second_part = 117440


class Computer:
    def __init__(self, input: str) -> None:
        self.A = int(input.split("\n")[0].split(" ")[-1])
        self.B = int(input.split("\n")[1].split(" ")[-1])
        self.C = int(input.split("\n")[2].split(" ")[-1])
        self.instructions = list(
            map(int, input.split("\n")[4].split(" ")[-1].split(","))
        )
        if len(input.split("\n")) > 6:
            self.solution = input.split("\n")[6].split(" ")[-1]
        self.instruction_pointer = 0
        self.output = ""

    def calculate_combo_operand(self, operand: int):
        if operand >= 0 and operand <= 3:
            return operand
        if operand == 4:
            return self.A
        if operand == 5:
            return self.B
        if operand == 6:
            return self.C
        raise ValueError("Invalid operand!")

    def adv(self, operand: int) -> None:
        self.A = int(self.A / 2 ** self.calculate_combo_operand(operand))

    def bxl(self, operand: int) -> None:
        self.B = self.B ^ operand

    def bst(self, operand: int) -> None:
        self.B = self.calculate_combo_operand(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.A == 0:
            return
        self.instruction_pointer = operand

    def bxc(self, _: int) -> None:
        self.B = self.B ^ self.C

    def out(self, operand: int) -> None:
        output = self.calculate_combo_operand(operand) % 8
        if self.output != "":
            self.output += ","
        self.output += str(output)

    def bdv(self, operand: int) -> None:
        self.B = int(self.A / 2 ** self.calculate_combo_operand(operand))

    def cdv(self, operand: int) -> None:
        self.C = int(self.A / 2 ** self.calculate_combo_operand(operand))


def parse(input: str) -> Computer:
    return Computer(input)


def execute_instruction(computer: Computer) -> None:
    instruction = computer.instructions[computer.instruction_pointer]
    operand = computer.instructions[computer.instruction_pointer + 1]
    if instruction == 0:
        computer.adv(operand)
    elif instruction == 1:
        computer.bxl(operand)
    elif instruction == 2:
        computer.bst(operand)
    elif instruction == 3:
        if computer.A != 0:
            computer.jnz(operand)
            return  # In this case the instruction pointer is not increased by 2..
    elif instruction == 4:
        computer.bxc(operand)
    elif instruction == 5:
        computer.out(operand)
    elif instruction == 6:
        computer.bdv(operand)
    elif instruction == 7:
        computer.cdv(operand)
    else:
        raise ValueError("Invalid instruction!")
    computer.instruction_pointer += 2


def run_program(computer: Computer) -> str:
    while computer.instruction_pointer >= 0 and computer.instruction_pointer + 1 < len(
        computer.instructions
    ):
        execute_instruction(computer)
    return computer.output


def solve_first_part(computer: Computer) -> str:
    return run_program(computer)


def step_back(computer: Computer, final_A: int, iteration: int) -> None:
    instructions = ",".join(map(str, computer.instructions))
    B = computer.B
    C = computer.C

    # The range is valid for any input that only changes A in one adv instruction with an operand of 3.
    for A in range(8 * final_A, 8 * final_A + 8):
        # Reset computer
        computer.A = A
        computer.B = B
        computer.C = C
        computer.instruction_pointer = 0
        computer.output = ""

        # Execute all instructions but the last (this is assumed to be the jnz, that resets the instruction pointer)
        while computer.instruction_pointer < len(computer.instructions) - 2:
            execute_instruction(computer)
        if computer.A == final_A and computer.output == str(
            computer.instructions[-iteration]
        ):
            if run_program(computer) == instructions:
                return A
            result = step_back(computer, A, iteration + 1)
            if result is not None:
                return result
    return None


def solve_second_part(computer: Computer) -> int:
    return step_back(computer, 0, 1)


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
    print("Reading inputs...")
    example_input = read_input_from_file(example_file)
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return

    example_computer = parse(example_input)
    original_example_computer = copy.deepcopy(example_computer)
    computer = parse(input)
    original_computer = copy.deepcopy(computer)

    print("\nSolving first part...")
    solve_part(
        example_computer,
        computer,
        solve_first_part,
        example_computer.solution,
    )

    print("\nSolving second part...")
    solve_part(
        original_example_computer,
        original_computer,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
