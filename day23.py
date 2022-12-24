import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day23_input1.txt')

# Read the input, save the elf positions as a dictionary where the key is a tuple of (row, column) and the value is None (for now)
elves = {}
row = 0
for line in input1:
    for column in range(len(line)):
        if line[column] == '#':
            elves[(row, column)] = None
    row += 1
input1.close()

# Given a position, return a dictionary of the coordinates in the 8 possible adjacent directions
def getAdjacentCoordinates(position):
    return {
        'NW': (position[0] - 1, position[1] - 1),
        'N': (position[0] - 1, position[1]),
        'NE': (position[0] - 1, position[1] + 1),
        'W': (position[0], position[1] - 1),
        'E': (position[0], position[1] + 1),
        'SW': (position[0] + 1, position[1] - 1),
        'S': (position[0] + 1, position[1]),
        'SE': (position[0] + 1, position[1] + 1)
    }

# Attempt to move all the elves
def moveElves(elves, directions):
    proposedPositions = {}
    for elf in elves:
        adjacentPositions = getAdjacentCoordinates(elf)
        # Don't try to move if there are no elves around you
        if sum([1 if adjacentPositions[adj] in elves else 0 for adj in adjacentPositions]) == 0:
            continue
        # Go through the directions in order
        # If an elf has a position they want to propose to move to, set the value in the dictionary to that position
        # Track all proposed positions in a dictionary, tracking how many elves propose that position
        for direction in directions:
            if direction == 'N' and adjacentPositions['NW'] not in elves and adjacentPositions['N'] not in elves and adjacentPositions['NE'] not in elves:
                elves[elf] = adjacentPositions['N']
                if adjacentPositions['N'] in proposedPositions:
                    proposedPositions[adjacentPositions['N']] += 1
                else:
                    proposedPositions[adjacentPositions['N']] = 1
                break
            elif direction == 'S' and adjacentPositions['SW'] not in elves and adjacentPositions['S'] not in elves and adjacentPositions['SE'] not in elves:
                elves[elf] = adjacentPositions['S']
                if adjacentPositions['S'] in proposedPositions:
                    proposedPositions[adjacentPositions['S']] += 1
                else:
                    proposedPositions[adjacentPositions['S']] = 1
                break
            elif direction == 'W' and adjacentPositions['NW'] not in elves and adjacentPositions['W'] not in elves and adjacentPositions['SW'] not in elves:
                elves[elf] = adjacentPositions['W']
                if adjacentPositions['W'] in proposedPositions:
                    proposedPositions[adjacentPositions['W']] += 1
                else:
                    proposedPositions[adjacentPositions['W']] = 1
                break
            elif direction == 'E' and adjacentPositions['NE'] not in elves and adjacentPositions['E'] not in elves and adjacentPositions['SE'] not in elves:
                elves[elf] = adjacentPositions['E']
                if adjacentPositions['E'] in proposedPositions:
                    proposedPositions[adjacentPositions['E']] += 1
                else:
                    proposedPositions[adjacentPositions['E']] = 1
                break
    # If there are no proposed positions, then the elves are all in position and we are done with Pt. 2
    if len(proposedPositions) == 0:
        return elves, directions[1:] + directions[0], True
    # Only grab the proposed positions that have a single-elf looking to move there
    acceptedPositions = set([position for position in proposedPositions if proposedPositions[position] == 1])
    # If an elf's proposal was accepted, move. Otherwise stay in place
    newElves = {}
    for elf in elves:
        if elves[elf] in acceptedPositions:
            newElves[elves[elf]] = None
        else:
            newElves[elf] = None
    # Return the new elf positions, and cycle the directions for next time
    return newElves, directions[1:] + directions[0], False

# Function for counting how many open spaces are in the smallest rectangle containing all elves
def countOpenSpaces(elves):
    minx = float('inf')
    maxx = -float('inf')
    miny = float('inf')
    maxy = -float('inf')
    for elf in elves:
        minx = min(elf[1], minx)
        maxx = max(elf[1], maxx)
        miny = min(elf[0], miny)
        maxy = max(elf[0], maxy)
    return ((maxx - minx + 1) * (maxy - miny + 1)) - len(elves)

# Function for printing out the grid (debug only)
def printGrid(elves):
    minx = float('inf')
    maxx = -float('inf')
    miny = float('inf')
    maxy = -float('inf')
    for elf in elves:
        minx = min(elf[1], minx)
        maxx = max(elf[1], maxx)
        miny = min(elf[0], miny)
        maxy = max(elf[0], maxy)
    grid = ''
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (y, x) in elves:
                grid += '#'
            else:
                grid += '.'
        grid += '\n'
    print(grid)

# Keep doing movement rounds until doneMoving is returned as True.
directions = 'NSWE'
doneMoving = False
round = 1
while not doneMoving:
    elves, directions, doneMoving = moveElves(elves, directions)
    # Pt. 1
    if round == 10:
        print("There are", countOpenSpaces(elves), "open spaces in the rectangle") 
    round += 1
print("The elves don't move starting on round", round - 1)
exit()