import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day17_input2.txt')
jetStreams = next(input1).strip()
input1.close()

# Constants and tracking variables
jetStreamIndex = 0
towerWidth = 7
towerHeight = 0
tower = [['.'] * towerWidth]
rockHeights = {
    1: 1,
    2: 3,
    3: 3,
    4: 4,
    5: 2
}
rowsChopped = 0

# Given a tower, count the number of non-blank rows
def getHeight(tower):
    blankRows = 0
    while blankRows < len(tower) and ''.join(tower[blankRows]) == '.' * towerWidth:
        blankRows += 1
    return len(tower) - blankRows + rowsChopped

# Drop the next rock onto the tower
def addRock(tower, rockNum):

    # Count how many blank rows are over the tower
    blankRows = 0
    while blankRows < len(tower) and ''.join(tower[blankRows]) == '.' * towerWidth:
        blankRows += 1
    # Add more blank rows if we need them to fit the current rock
    if blankRows < 3 + rockHeights[rockNum]:
        for _ in range(3 - blankRows + rockHeights[rockNum]):
            tower = [['.'] * towerWidth] + tower
    # Remove blank rows if there are too many for the current rock
    else:
        tower = tower[blankRows - (3 + rockHeights[rockNum]):]

    # Add the newly falling rock. Track its position.
    bottomRow = None
    topRow = 0
    if rockNum == 1:
        tower[0] = [*'..@@@@.']
        bottomRow = 0
    elif rockNum == 2:
        tower[0] = [*'...@...']
        tower[1] = [*'..@@@..']
        tower[2] = [*'...@...']
        bottomRow = 2
    elif rockNum == 3:
        tower[0] = [*'....@..']
        tower[1] = [*'....@..']
        tower[2] = [*'..@@@..']
        bottomRow = 2
    elif rockNum == 4:
        tower[0] = [*'..@....']
        tower[1] = [*'..@....']
        tower[2] = [*'..@....']
        tower[3] = [*'..@....']
        bottomRow = 3
    elif rockNum == 5:
        tower[0] = [*'..@@...']
        tower[1] = [*'..@@...']
        bottomRow = 1
    
    global jetStreamIndex, towerHeight, rowsChopped

    # Keep going until the rock comes to a halt.
    while True:
        movementDirection = jetStreams[jetStreamIndex]
        jetStreamIndex = (jetStreamIndex + 1) % len(jetStreams)

        # Determine if the jet streams can push the rock
        canMoveSide = True
        for row in range(topRow, bottomRow + 1):
            if movementDirection == '>':
                rightEdge = towerWidth - tower[row][::-1].index('@')
                if rightEdge >= towerWidth or tower[row][rightEdge] != '.':
                    canMoveSide = False
            else:
                leftEdge = tower[row].index('@') - 1
                if leftEdge < 0 or tower[row][leftEdge] != '.':
                    canMoveSide = False

        # Push the rock if it can be pushed
        if canMoveSide:
            for row in range(topRow, bottomRow + 1):
                if movementDirection == '>':
                    tower[row][towerWidth - tower[row][::-1].index('@')] = '@'
                    tower[row][tower[row].index('@')] = '.'
                else:
                    tower[row][tower[row].index('@') - 1] = '@'
                    tower[row][towerWidth - tower[row][::-1].index('@') - 1] = '.'

        # See if the rock can fall down
        canMoveDown = True
        for row in range(topRow, bottomRow + 1):
            # True if the rock has hit the floor
            if row + 1 == len(tower):
                canMoveDown = False
                break
            else:
                indices = [i for i, x in enumerate(tower[row]) if x == '@']
                for index in indices:
                    if tower[row + 1][index] == '#':
                        canMoveDown = False
                        break
                if not canMoveDown:
                    break

        # Drop the rock one row if it can fall
        if canMoveDown:
            for row in range(bottomRow, topRow - 1, -1):
                indices = [i for i, x in enumerate(tower[row]) if x == '@']
                for index in indices:
                    tower[row + 1][index] = '@'
                    tower[row][index] = '.'
            bottomRow += 1
            topRow += 1
        
        # Rock can't fall, time to come to a halt
        else:
            choppingValue = None
            # Change the rock from '@' symbols to '#' symbols
            for row in range(topRow, bottomRow + 1):
                for column in range(towerWidth):
                    if tower[row][column] == '@':
                        tower[row][column] = '#'
                # If we have a fully filled row, call a Tetris and chop off the tower from there, everything below that doesn't matter anymore
                # (except the number of rows chopped, for height-tracking purposes)
                if not choppingValue and ''.join(tower[row]) == '#' * towerWidth:
                    choppingValue = row
            if choppingValue:
                rowsChopped += len(tower[choppingValue:])
                tower = tower[0:choppingValue]            

            # Update the tower's height   
            blankRows = 0
            while blankRows < len(tower) and ''.join(tower[blankRows]) == '.' * towerWidth:
                blankRows += 1
            towerHeight = getHeight(tower)
            break
    return tower

trillion = 1000000000000
x = 0
targetStateRock = 6294
targetState = None
targetStateHeight = None
targetStateRowsChopped = None
while x < trillion:
    # Next rock
    tower = addRock(tower, (x % 5) + 1)
    # Part 1
    if x == 2021:
        print("After 2022 rocks, the tower is", towerHeight, "rows tall")
    # Part 2 - pick an arbitrary state of rockNumber and jetStreamIndex. See how long it takes to see this state again.
    # The theory is to find a cycle and use that to skip ahead to the end. 1 trillion would take forever manually.
    elif x == targetStateRock:
        targetState = ((x % 5) + 1, jetStreamIndex)
        targetStateHeight = getHeight(tower)
        targetStateRowsChopped = rowsChopped
    elif x > targetStateRock:
        currentState = ((x % 5) + 1, jetStreamIndex)
        # Bingo, we've found a cycle. Track how many rocks are between cycles, along with how many rows get chopped.
        # Use these values to skip ahead to the final cycle and run manually to the finish line
        if currentState == targetState:
            rocksInCycle = x - targetStateRock
            cycleRowsChopped = rowsChopped - targetStateRowsChopped
            cyclesToAdd = (trillion - x) // rocksInCycle
            x += (rocksInCycle * cyclesToAdd)
            rowsChopped += (cycleRowsChopped * cyclesToAdd)
    x += 1

print("After 1 trillion rocks, the tower is", towerHeight, "rows tall")
exit()