# Read input.txt and create two lists from it:
input = open("example.txt", "r")
list1 = []
list2 = []
for line in input:
    x, y = line.split()
    list1.append(int(x))
    list2.append(int(y))

list1.sort()
list2.sort()

# Iterate over both lists and add the total distances between the numbers in the lists:
total = 0
for i in range(len(list1)):
    total += abs(list1[i] - list2[i])

print("The total distance between the two lists is: ", total)