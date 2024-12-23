import pathlib
from typing import List, Set, Tuple
import copy
import time

# The expected solutions for the example input of the first and second part of the puzzle used for checking the implemented algorithm.
example_file = "example.txt"
given_example_solution_of_first_part = 7
given_example_solution_of_second_part = "co,de,ka,ta"


def parse(input: str) -> List[Tuple[str, str]]:
    return [tuple(line.split("-")) for line in input.splitlines()]


# def solve_first_part(connections: List[Tuple[str, str]]) -> int:
#     networks = []
#     for connection in connections:
#         matching_networks = []
#         for network in networks:
#             if connection[0] in network or connection[1] in network:
#                 matching_networks.append(network)
#         if len(matching_networks) == 0:
#             networks.append(set(connection))
#         elif len(matching_networks) == 1:
#             matching_networks[0].add(connection[0])
#             matching_networks[0].add(connection[1])
#         else:
#             for matching_network in matching_networks[1:]:
#                 matching_networks[0].update(matching_network)
#                 networks.remove(matching_network)
#     return len([network for network in networks if len(network) == 3])


def find_networks_of_three_computers(connections: List[Tuple[str, str]]) -> Set[str]:
    three_computer_networks = set()
    for a, b in connections:
        for c, d in connections:
            if (a, b) == (c, d):
                continue
            if a == c:
                if (b, d) in connections:
                    three_computer_networks.add(",".join(sorted([a, b, d])))
            elif a == d:
                if (b, c) in connections:
                    three_computer_networks.add(",".join(sorted([a, b, c])))
            elif b == c:
                if (a, d) in connections:
                    three_computer_networks.add(",".join(sorted([a, b, d])))
            elif b == d:
                if (a, c) in connections:
                    three_computer_networks.add(",".join(sorted([a, b, c])))

    return three_computer_networks


def solve_first_part(connections: List[Tuple[str, str]]) -> int:
    return len(
        [
            network
            for network in find_networks_of_three_computers(connections)
            if ",t" in network or network.startswith("t")
        ]
    )


def solve_second_part(connections: List[Tuple[str, str]]) -> str:
    computers = set()
    for connection in connections:
        for computer in connection:
            computers.add(computer)

    fully_connected_computers = list(find_networks_of_three_computers(connections))

    begin = time.time()
    for index, computer in enumerate(computers):
        if index % 10 == 0:
            print(
                f"Processing computer {index}/{len(computers)} took a total of {time.time()-begin} seconds."
            )
        for network in fully_connected_computers:
            if computer in network:
                continue
            computer_is_connected_with_every_computer_in_network = True
            for network_computer in network.split(","):
                if (computer, network_computer) not in connections and (
                    network_computer,
                    computer,
                ) not in connections:
                    computer_is_connected_with_every_computer_in_network = False
                    break
            if computer_is_connected_with_every_computer_in_network:
                fully_connected_computers[fully_connected_computers.index(network)] = (
                    ",".join(sorted(network.split(",") + [computer]))
                )

    return max(fully_connected_computers, key=len)


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

    example_connections = parse(example_input)
    connections = parse(input)

    print("\nSolving first part...")
    solve_part(
        example_connections,
        connections,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_connections,
        connections,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
