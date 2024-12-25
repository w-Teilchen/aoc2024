import pathlib

# The given solutions need to be updated to the correct values.
given_example_solution_of_first_part = 2
given_example_solution_of_second_part = 4


def parse(input):
    return [list(map(int, line.split(" "))) for line in input.strip().split("\n")]


def is_stable_sequence(sequence):
    increments = [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]
    return all([abs(increment) <= 3 for increment in increments]) and (
        all([increment < 0 for increment in increments])
        or all([increment > 0 for increment in increments])
    )


def solve_first_part(numbers):
    number_of_stable_sequences = 0
    for sequence in numbers:
        if is_stable_sequence(sequence):
            number_of_stable_sequences += 1
    return number_of_stable_sequences


def solve_second_part(numbers):
    number_of_stable_sequences = 0
    for sequence in numbers:
        if is_stable_sequence(sequence):
            number_of_stable_sequences += 1
        else:
            for i in range(1, len(sequence) + 1):
                if is_stable_sequence(sequence[: i - 1] + sequence[i:]):
                    number_of_stable_sequences += 1
                    break
    return number_of_stable_sequences


def main():
    for path in ["example.txt", "input.txt"]:
        input = pathlib.Path(path).read_text().strip()

        numbers = parse(input)
        first_solution = solve_first_part(numbers)
        if path == "example.txt":
            assert (
                first_solution == given_example_solution_of_first_part
            ), f"The calculated value {first_solution} did not match the given solution {given_example_solution_of_first_part}."
            print("The solution to the first part was correctly calculated.")
        else:
            print(f"The solution to the first part is {first_solution}.")

        second_solution = solve_second_part(numbers)
        if path == "example.txt":
            assert (
                second_solution == given_example_solution_of_second_part,
                f"The calculated value {second_solution} did not match the given solution {given_example_solution_of_second_part}.",
            )
            print("The solution to the second part was correctly calculated.")
        else:
            print(f"The solution to the second part is {second_solution}.")


if __name__ == "__main__":
    main()
