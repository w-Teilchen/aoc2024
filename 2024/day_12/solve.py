import pathlib
from typing import List, Tuple

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 1930
given_example_solution_of_second_part = 1206


class Region:
    def __init__(self, x: int, y: int, plant_type: str):
        self.plots = {(x, y)}
        self.plant_type = plant_type

    def extend(self, map: List[List[str]], x: int, y: int):
        if x - 1 >= 0 and map[x - 1][y] == self.plant_type:
            self.plots.add((x - 1, y))
            map[x - 1][y] = "."
            self.extend(map, x - 1, y)
        if x + 1 < len(map) and map[x + 1][y] == self.plant_type:
            self.plots.add((x + 1, y))
            map[x + 1][y] = "."
            self.extend(map, x + 1, y)
        if y - 1 >= 0 and map[x][y - 1] == self.plant_type:
            self.plots.add((x, y - 1))
            map[x][y - 1] = "."
            self.extend(map, x, y - 1)
        if y + 1 < len(map[0]) and map[x][y + 1] == self.plant_type:
            self.plots.add((x, y + 1))
            map[x][y + 1] = "."
            self.extend(map, x, y + 1)

    def calculate_area(self):
        return len(self.plots)

    def calculate_circumference(self):
        circumference = 0
        for plot in self.plots:
            if (plot[0] - 1, plot[1]) not in self.plots:
                circumference += 1
            if (plot[0] + 1, plot[1]) not in self.plots:
                circumference += 1
            if (plot[0], plot[1] - 1) not in self.plots:
                circumference += 1
            if (plot[0], plot[1] + 1) not in self.plots:
                circumference += 1

        return circumference

    def display(self):
        minimum_x = min([x for x, y in self.plots])
        maximum_x = max([x for x, y in self.plots])
        minimum_y = min([y for x, y in self.plots])
        maximum_y = max([y for x, y in self.plots])
        for y in range(minimum_y, maximum_y + 1):
            for x in range(minimum_x, maximum_x + 1):
                if (x, y) in self.plots:
                    print(self.plant_type, end="")
                else:
                    print(" ", end="")
            print()

    def calculate_number_of_edges(self):
        potential_edges = []
        for plot in self.plots:
            if (plot[0] + 1, plot[1]) not in self.plots:
                potential_edges.append(
                    Edge(plot, is_horizontal=False, is_left_or_lower_plot_inside=True)
                )
            if (plot[0] - 1, plot[1]) not in self.plots:
                potential_edges.append(
                    Edge(
                        (plot[0] - 1, plot[1]),
                        is_horizontal=False,
                        is_left_or_lower_plot_inside=False,
                    )
                )
            if (plot[0], plot[1] + 1) not in self.plots:
                potential_edges.append(
                    Edge(plot, is_horizontal=True, is_left_or_lower_plot_inside=True)
                )
            if (plot[0], plot[1] - 1) not in self.plots:
                potential_edges.append(
                    Edge(
                        (plot[0], plot[1] - 1),
                        is_horizontal=True,
                        is_left_or_lower_plot_inside=False,
                    )
                )

        potential_edges.sort(
            key=lambda edge: (
                edge.edge_plot[0] if edge.is_horizontal else edge.edge_plot[1]
            )
        )
        edges = []
        for potential_edge in potential_edges:
            not_part_of_existing_edge = True
            for edge in edges:
                if edge.extends_edge(potential_edge):
                    edge.extend(potential_edge)
                    not_part_of_existing_edge = False
                    break
            if not_part_of_existing_edge:
                edges.append(CombinedEdge(potential_edge))

        return len(edges)


class Edge:
    def __init__(
        self,
        edge_plot: Tuple[int, int],
        is_horizontal: bool,
        is_left_or_lower_plot_inside: bool,
    ):
        self.edge_plot = edge_plot
        self.is_horizontal = is_horizontal
        self.is_left_plot_inside = is_left_or_lower_plot_inside


class CombinedEdge:
    def __init__(self, edge: Edge):
        self.edges = {edge}
        self.is_horizontal = edge.is_horizontal

    def extends_edge(self, extending_edge: Edge):
        if self.is_horizontal != extending_edge.is_horizontal:
            return False
        if self.is_horizontal:
            for edge in self.edges:
                if (
                    extending_edge.edge_plot[1] == edge.edge_plot[1]
                    and extending_edge.edge_plot[0]
                    in [edge.edge_plot[0] - 1, edge.edge_plot[0] + 1]
                    and extending_edge.is_left_plot_inside == edge.is_left_plot_inside
                ):
                    return True
        else:
            for edge in self.edges:
                if (
                    extending_edge.edge_plot[0] == edge.edge_plot[0]
                    and extending_edge.edge_plot[1]
                    in [
                        edge.edge_plot[1] - 1,
                        edge.edge_plot[1] + 1,
                    ]
                    and extending_edge.is_left_plot_inside == edge.is_left_plot_inside
                ):
                    return True
        return False

    def extend(self, edge: Edge):
        self.edges.add(edge)


def parse(input: str) -> List[List[int]]:
    return [list(line) for line in input.strip().split("\n")]


def find_regions(map: List[List[int]]) -> List[Region]:
    regions = []
    for x, row in enumerate(map):
        for y, plant_type in enumerate(row):
            if plant_type == ".":
                continue
            regions.append(Region(x, y, plant_type))
            regions[-1].extend(map, x, y)
    return regions


def solve_first_part(regions: List[Region]) -> int:
    price_for_fences = 0
    for region in regions:
        price_for_fences += region.calculate_circumference() * region.calculate_area()
    return price_for_fences


def solve_second_part(regions: List[Region]) -> int:
    price_for_fences = 0
    for region in regions:
        if region.plant_type == "O":
            region.display()
        print(f"Region has {region.calculate_number_of_edges()} edges.")
        price_for_fences += region.calculate_number_of_edges() * region.calculate_area()
    return price_for_fences


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
    example_regions: List[Region],
    regions: List[Region],
    solver: callable,
    given_solution: int,
):
    calculated_solution = solver(example_regions)
    assert (
        calculated_solution == given_solution
    ), f"The calculated value {calculated_solution} did not match the given solution {given_solution}."
    print("The solution for the example input was correctly reproduced.")

    calculated_solution = solver(regions)
    print(f"The solution to the input is {calculated_solution}")


def main():
    print("Reading inputs...")
    example_input = read_input_from_file("example.txt")
    input = read_input_from_file("input.txt")
    if example_input is None or input is None:
        return
    example_map = parse(example_input)
    map = parse(input)
    example_regions = find_regions(example_map)
    regions = find_regions(map)

    print("\nSolving first part...")
    solve_part(
        example_regions, regions, solve_first_part, given_example_solution_of_first_part
    )

    print("\nSolving second part...")
    solve_part(
        example_regions,
        regions,
        solve_second_part,
        given_example_solution_of_second_part,
    )


if __name__ == "__main__":
    main()
