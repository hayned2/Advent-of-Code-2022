import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day1_input1.txt')
chunkiest_elves = [0, 0, 0]
current_elf = 0
for line in input1:
    if not line.isspace():
        current_elf += int(line)
    else:
        chunkiest_elves.append(current_elf)
        chunkiest_elves.sort()
        chunkiest_elves = chunkiest_elves[1:]
        current_elf = 0
print("The elf with the most calories is carrying", chunkiest_elves[-1])
print("The three elves carrying the most calories are carrying", sum(chunkiest_elves))
