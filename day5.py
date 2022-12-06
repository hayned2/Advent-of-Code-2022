import os
import re
import copy

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day5_input1.txt')
columns = {}

# Start by building up the initial configuration. Coded to not know how many columns there are.
# But we assume that there will be at least one crate in each column to start with.
for line in input1:
    prevColumn = 0
    while True:
        column = (line.find('[', prevColumn))
        if column != -1:
            if (column // 4) not in columns:
                columns[column // 4] = []
            columns[column // 4].append(line[column + 1])
            prevColumn = column + 1
        else:
            break
    # Stop going through lines once we hit one that doesn't have a crate (the list of column IDs)
    if line.find('[') == -1:
        break

columns2 = copy.deepcopy(columns)

# Skip the blank line between the list of column IDs and the movement instructions
next(input1)

for line in input1:
    [quantity, source, destination] = [int(value) for value in re.findall(r'\d+', line)]
    source -= 1
    destination -= 1

    movedBoxes = columns[source][0:quantity]
    movedBoxes.reverse()
    columns[source] = columns[source][quantity:]
    columns[destination] = movedBoxes + columns[destination]

    movedBoxes2 = columns2[source][0:quantity]
    columns2[source] = columns2[source][quantity:]
    columns2[destination] = movedBoxes2 + columns2[destination]

print("A CrateMover9000 would result in the following box configuration:", ''.join([columns[id][0] for id in sorted(columns.keys())]))
print("A CrateMover9001 would result in the following box configuration:", ''.join([columns2[id][0] for id in sorted(columns2.keys())]))