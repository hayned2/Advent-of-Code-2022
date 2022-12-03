import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day3_input1.txt')
score = 0
badgeScore = 0
bags = []

# Uppercase characters have ascii values of 65-91. Lowercase have values of 97-122
def getValue(item):
    if item.isupper():
        return ord(item) - 38
    else:
        return ord(item) - 96

for line in input1:
    line = line.strip()
    item = next(iter(set(line[0:len(line) // 2]).intersection(set(line[len(line) // 2:]))))
    score += getValue(item)
    bags.append(line)
    if len(bags) == 3:
        badge = next(iter(set(bags[0]).intersection(set(bags[1]).intersection(set(bags[2])))))
        badgeScore += getValue(badge)
        bags = []

print("The priority sum of all items is:", score)
print("The priority of the badges is:", badgeScore)

input1.close()
exit()