import pathlib
from typing import Dict, List, Tuple

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 14
given_example_solution_of_second_part = 34


class Antenna:
    def __init__(self, x: int, y: int, f: str):
        self.x = x
        self.y = y
        self.f = f

    def get_distance(self, x: int, y: int) -> Tuple[int]:
        return [self.x - x, self.y - y]


def parse(input: str) -> List[List[int]]:
    antennas = {}
    for y, line in enumerate(input.split("\n")):
        for x, f in enumerate(list(line)):
            if f != ".":
                if f in antennas:
                    antennas[f].append(Antenna(x, y, f))
                else:
                    antennas[f] = [Antenna(x, y, f)]
    return antennas


def solve_first_part(
    map_dimensions: Tuple[int, int], antennas: Dict[str, List[Antenna]]
) -> int:
    number_of_tiles_with_resonances = 0
    for y in range(map_dimensions[0]):
        for x in range(map_dimensions[1]):
            resonance_found = False
            for frequency in antennas:
                if resonance_found:
                    break
                distances = []
                for antenna in antennas[frequency]:
                    distances.append(antenna.get_distance(x, y))
                for distance in distances:
                    if distance == [0, 0]:
                        continue
                    if [-2 * distance[0], -2 * distance[1]] in distances or [
                        2 * distance[0],
                        2 * distance[1],
                    ] in distances:
                        number_of_tiles_with_resonances += 1
                        resonance_found = True
                        break
    return number_of_tiles_with_resonances


def find_resonance(distances: List[Tuple[int]]) -> bool:
    if [0, 0] in distances:
        return True
    for distance in distances:
        for other_distance in distances:
            if distance == other_distance:  # don't compare a distance with itself
                continue
            if distance[1] == 0 or other_distance[1] == 0:
                if distance[1] == 0 and other_distance[1] == 0:
                    return True
                continue

            if distance[0] / distance[1] == other_distance[0] / other_distance[1]:
                return True
    return False


def solve_second_part(
    map_dimensions: Tuple[int, int], antennas: Dict[str, List[Antenna]]
) -> int:
    number_of_tiles_with_resonances = 0
    for y in range(map_dimensions[0]):
        for x in range(map_dimensions[1]):
            if x == 5 and y == 2:
                print("debug")
            resonance_found = False
            for frequency in antennas:
                if resonance_found:
                    break
                distances = []
                for antenna in antennas[frequency]:
                    distances.append(antenna.get_distance(x, y))
                resonance_found = find_resonance(distances)
                if resonance_found:
                    number_of_tiles_with_resonances += 1
                    break

    return number_of_tiles_with_resonances


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
    example_dimensions: Tuple[int, int],
    example_antennas: Dict[str, List[Antenna]],
    dimensions: Tuple[int, int],
    antennas: Dict[str, List[Antenna]],
    solver: callable,
    given_solution: int,
):
    calculated_solution = solver(example_dimensions, example_antennas)
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(dimensions, antennas)
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return
    example_antennas = parse(example_input)
    example_dimensions = (
        len(example_input.split("\n")[0]),
        len(example_input.split("\n")),
    )
    antennas = parse(input)
    dimensions = (len(input.split("\n")[0]), len(input.split("\n")))

    print("\nSolving first part...")
    solve_part(
        example_dimensions,
        example_antennas,
        dimensions,
        antennas,
        solve_first_part,
        given_example_solution_of_first_part,
    )

    print("\nSolving second part...")
    solve_part(
        example_dimensions,
        example_antennas,
        dimensions,
        antennas,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
