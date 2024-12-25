# Read input.txt and create two lists from it:
input = open("input.txt", "r")
list1 = []
list2 = []
for line in input:
    x, y = line.split()
    list1.append(int(x))
    list2.append(int(y))

# Create dictionaries to store the counts of each number in the lists:
count1 = {num: list1.count(num) for num in list1}
count2 = {num: list2.count(num) for num in list2}

# Calcute the similarity score of the two lists (sum of the product of the counts of each number in both lists):
similarity  = 0
for num in count1:
    if num in count2:
        similarity  += num * count1[num] * count2[num]

print("The total similarity score of the two lists is: ", similarity)