import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day4_input1.txt')

containments = 0
overlaps = 0
for line in input1:
    line = line.strip().split(',')
    elf1 = [int(num) for num in line[0].split('-')]
    elf2 = [int(num) for num in line[1].split('-')]
    if (elf1[0] <= elf2[0] and elf1[1] >= elf2[1]) or (elf2[0] <= elf1[0] and elf2[1] >= elf1[1]):
        containments += 1
        overlaps += 1
    elif (elf1[0] <= elf2[1] and elf1[1] >= elf2[0]):
        overlaps += 1
print("Total elf pairs with total overlap:", containments)
print("Total number of overlapping pairs:", overlaps)

input1.close()
exit()