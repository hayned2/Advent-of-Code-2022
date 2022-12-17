import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day17_input2.txt')
jetStreams = next(input1).strip()
jetStreamIndex = 0
input1.close()

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

def getHeight(tower):
    blankRows = 0
    while blankRows < len(tower) and ''.join(tower[blankRows]) == '.' * towerWidth:
        blankRows += 1
    return len(tower) - blankRows + rowsChopped

def addRock(tower, rockNum):

    blankRows = 0
    while blankRows < len(tower) and ''.join(tower[blankRows]) == '.' * towerWidth:
        blankRows += 1
    if blankRows < 3 + rockHeights[rockNum]:
        for _ in range(3 - blankRows + rockHeights[rockNum]):
            tower = [['.'] * towerWidth] + tower
    else:
        tower = tower[blankRows - (3 + rockHeights[rockNum]):]

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

    while True:
        movementDirection = jetStreams[jetStreamIndex]
        jetStreamIndex = (jetStreamIndex + 1) % len(jetStreams)
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
        if canMoveSide:
            for row in range(topRow, bottomRow + 1):
                if movementDirection == '>':
                    tower[row][towerWidth - tower[row][::-1].index('@')] = '@'
                    tower[row][tower[row].index('@')] = '.'
                else:
                    tower[row][tower[row].index('@') - 1] = '@'
                    tower[row][towerWidth - tower[row][::-1].index('@') - 1] = '.'
        canMoveDown = True
        for row in range(topRow, bottomRow + 1):
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

        if canMoveDown:
            for row in range(bottomRow, topRow - 1, -1):
                indices = [i for i, x in enumerate(tower[row]) if x == '@']
                for index in indices:
                    tower[row + 1][index] = '@'
                    tower[row][index] = '.'
            bottomRow += 1
            topRow += 1
        else:
            choppingValue = None
            for row in range(topRow, bottomRow + 1):
                for column in range(towerWidth):
                    if tower[row][column] == '@':
                        tower[row][column] = '#'
                if not choppingValue and ''.join(tower[row]) == '#' * towerWidth:
                    choppingValue = row
            if choppingValue:
                rowsChopped += len(tower[choppingValue:])
                tower = tower[0:choppingValue]

            # columnHeights = {}
            # unfoundHeights = set(range(towerWidth))
            # currentRow = 0
            # while len(unfoundHeights) > 0 and currentRow < len(tower):
            #     for column in unfoundHeights:
            #         if tower[currentRow][column] == '#':
            #             columnHeights[column] = currentRow
            #     unfoundHeights -= set(columnHeights.keys())
            #     currentRow += 1
            # if len(unfoundHeights) == 0:
            #     choppingValue = max(columnHeights.values())
            #     rowsChopped += len(tower[choppingValue:])
            #     #print("Chopping off", len(tower[choppingValue:]), "rows", rowsChopped)
            #     #print('BEFORE\n' + '\n'.join(''.join(row) for row in tower))
            #     tower = tower[0:choppingValue]
            #     #print('AFTER\n' + '\n'.join(''.join(row) for row in tower))
            
                    
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
    tower = addRock(tower, (x % 5) + 1)
    #print('\n' + '\n'.join(''.join(row) for row in tower))
    if x == 2021:
        print("After 2022 rocks, the tower is", towerHeight, "tall")
    elif x == targetStateRock:
        targetState = ((x % 5) + 1, jetStreamIndex)
        targetStateHeight = getHeight(tower)
        targetStateRowsChopped = rowsChopped
    elif x > targetStateRock:
        currentState = ((x % 5) + 1, jetStreamIndex)
        if currentState == targetState:
            print("CYCLE FOUND AT", x)
            rocksInCycle = x - targetStateRock
            cycleRowsChopped = rowsChopped - targetStateRowsChopped
            print("Cycle is", rocksInCycle, "rocks long, with rows chopped", cycleRowsChopped)
            cyclesToAdd = (trillion - x) // rocksInCycle
            x += (rocksInCycle * cyclesToAdd)
            rowsChopped += (cycleRowsChopped * cyclesToAdd)
            print("Skipping", cyclesToAdd, "cycles to rock", x, "chopped", rowsChopped)

    x += 1

print("After 1 trillion rocks, the tower is", towerHeight, "tall")
