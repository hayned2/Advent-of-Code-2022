import os

# Read the input, store the locations of the blizzards
input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day24_input3.txt')
blizzards = {}
row = 0
column = 0
for line in input1:
    line = line.strip()
    column = 0
    for character in line:
        if character in '><v^':
            if (row, column) in blizzards:
                blizzards[(row, column)].add(character)
            else:
                blizzards[(row, column)] = set([character])
        column += 1
    row += 1
input1.close()

# Initialize constants about the map
HEIGHT = row
WIDTH = column
SOURCE = (0, 1)
DESTINATION = (HEIGHT - 1, WIDTH - 2)

# Move the blizzards one step forward, wrapping around as needed
def moveBlizzards(blizzards):
    newBlizzards = {}
    for blizzard in blizzards:
        (row, column) = blizzard
        for direction in blizzards[blizzard]:
            newRow = row
            newColumn = column
            if direction == '>':
                newColumn = 1 if column + 1 == WIDTH - 1 else column + 1
            elif direction == '<':
                newColumn = WIDTH - 2 if column - 1 == 0 else column - 1
            elif direction == 'v':
                newRow = 1 if row + 1 == HEIGHT - 1 else row + 1
            elif direction == '^':
                newRow = HEIGHT - 2 if row - 1 == 0 else row - 1
            if (newRow, newColumn) in newBlizzards:
                newBlizzards[(newRow, newColumn)].add(direction)
            else:
                newBlizzards[(newRow, newColumn)]= set([direction])
    return newBlizzards

# Print the current state of the blizzards and elves (for debug purposes)
def printMap(blizzards, currentPosition):
    valley = []
    valley.append(['#'] * WIDTH)
    valley[0][1] = '.'
    for row in range(1, HEIGHT - 1):
        valleyRow = []
        for column in range(1, WIDTH - 1):
            if (row, column) in blizzards:
                if len(blizzards[(row, column)]) > 1:
                    valleyRow.append(str(len(blizzards[(row, column)])))
                else:
                    valleyRow.append(next(iter(blizzards[(row, column)])))
            elif (row, column) == currentPosition:
                valleyRow.append('E')
            else:
                valleyRow.append('.')
        valley.append(['#'] + valleyRow + ['#'])
    valley.append(['#'] * WIDTH)
    valley[-1][-2] = '.'
    print('\n'.join([''.join(valleyRow) for valleyRow in valley]) + '\n')

# The blizzards will cycle infinitely, so instead of calculating them over and over, assign each cycle state a number and save them
def countCycles(blizzards):
    cycles = {0: blizzards.copy()}
    cycleCount = 1
    while True:
        blizzards = moveBlizzards(blizzards)
        if blizzards == cycles[0]:
            break
        else:
            cycles[cycleCount] = blizzards
        cycleCount += 1
    return cycles
CYCLES = countCycles(blizzards)

# Get the next cycle number following a given cycle
def getNextCycle(cycle):
    return (cycle + 1) % len(CYCLES)

# Given a list of states, find the state with the lowest path length
def getShortestOption(queue):
    shortestPath = float('inf')
    bestOption = None
    for state in queue:
        if queue[state] < shortestPath:
            shortestPath = queue[state]
            bestOption = state
    return bestOption

# The main function, based off of Dijkstra's Algorithm
def maneuverValley(startingPosition, endingPosition, startingCycle):
    
    # Initialize our queue. A state is defined as a tuple of the position and the current cycle for the blizzards
    queue = {
        (startingPosition, startingCycle): 0
    }

    # Track which states we have already seen
    visited = set()

    # Keep going until we run out of states to try (shouldn't happen if the destination is reachable)
    while len(queue) > 0:

        # Find the next unvisited state with the shortest path leading to it
        # Remove that state from the queue, add it to visited. Grab the blizzard positions for that cycle.
        currState = getShortestOption(queue)
        ((currRow, currCol), currCycle) = currState
        currPath = queue[currState]
        del queue[currState]
        visited.add(currState)
        nextCycle = getNextCycle(currCycle)
        blizzards = CYCLES[nextCycle]

        # 5 options: Move up, down, left, right, or wait.
        newPositions = [(currRow + 1, currCol), (currRow - 1, currCol), (currRow, currCol + 1), (currRow, currCol - 1), (currRow, currCol)]
        for newPosition in newPositions:
            # If we reached our goal, we're done! Return the length of the path and the cycle we ended on.
            if newPosition == endingPosition:
                return currPath + 1, nextCycle
            # To add a new state to the queue, it must satisfy all of the following criteria:
            #   - Must be in bounds OR must be the starting position
            #   - Must not have been visited already
            #   - Is not obstructed by a blizzard in the next cycle
            #   - Is not already in the queue OR is in the queue with a longer path leading to it (update the queue entry for the latter)
            elif ((newPosition[0] < HEIGHT - 1 and newPosition[0] > 0 and \
                newPosition[1] < WIDTH - 1 and newPosition[1] > 0) or newPosition == startingPosition) and \
                (newPosition, nextCycle) not in visited and newPosition not in blizzards and \
                ((newPosition, nextCycle) not in queue or queue[(newPosition, nextCycle)] > currPath + 1):
                queue[(newPosition, nextCycle)] = currPath + 1

# I am making the assumption that the fastest path for all 3 trips is the combination of the 3 individual trips
totalPath = 0
path, cycle = maneuverValley(SOURCE, DESTINATION, 0)
print("The shortest path you can take to the exit is", path, "minutes")
totalPath += path

path, cycle = maneuverValley(DESTINATION, SOURCE, cycle)
print("The return trip to get the snacks is", path, "minutes")
totalPath += path

path, cycle = maneuverValley(SOURCE, DESTINATION, cycle)
print("The return-return trip back to the exit is", path, "minutes")
totalPath += path

print("The total of the three trips is", totalPath)
exit()