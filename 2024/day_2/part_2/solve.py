def is_stable_sequence(sequence):
    increments = [sequence[i] - sequence[i-1] for i in range(1, len(sequence))]
    return all([abs(increment) <= 3 and increment != 0 for increment in increments]) and (all([increment < 0 for increment in increments]) or all([increment > 0 for increment in increments]))

# Read input.txt and create lists of lists from it
input = open("input.txt", "r")

number_of_stable_sequences = 0
for line in input:
    sequence = list(map(int, line.strip().split(" ")))
    if is_stable_sequence(sequence):
        number_of_stable_sequences += 1
    else:
        for i in range(1, len(sequence) + 1):
            if is_stable_sequence(sequence[:i-1] + sequence[i:]):
                number_of_stable_sequences += 1
                break

print(number_of_stable_sequences, "stable sequences found.")

input.close()
