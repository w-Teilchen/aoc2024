# Read input.txt and create lists of lists from it
input = open("input.txt", "r")

number_of_stable_sequences = 0
for line in input:
    sequence = list(map(int, line.strip().split(" ")))
    increments = [sequence[i] - sequence[i-1] for i in range(1, len(sequence))]
    if all([abs(increment) <= 3 for increment in increments]):
        if all([increment < 0 for increment in increments]) or all([increment > 0 for increment in increments]):
            number_of_stable_sequences += 1

print(number_of_stable_sequences, "stable sequences found.")