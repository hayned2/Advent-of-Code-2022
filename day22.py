import os
import re

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day22_input1.txt')

# Read the input
mapLines = input1.readlines()
input1.close()
instructions = mapLines.pop()
mapLines.pop()

# mapLines is a list of strings representing the map, with whitespace padding
# Instructions uses regex to split it between the letter and number instructions
mapLines = [line.replace('\n', '') for line in mapLines]
width = max(len(line) for line in mapLines)
height = len(mapLines)
mapLines = [line.ljust(width) for line in mapLines]
instructions = re.split(r"(\d+)", instructions)[1:-1]
directions = '>v<^'

# Change the way you are facing given 'R' or 'L'
def rotate(facing, direction):
    return directions[(directions.index(facing) + (1 if direction == 'R' else -1)) % 4]

# Update the mapLines string to visualize our position (for printing purposes only)
def updateMap(mapLines, currentPos, facing):
    line = [*mapLines[currentPos[0]]]
    line[currentPos[1]] = facing
    mapLines[currentPos[0]] = ''.join(line)

# Print the map
def printMap(mapLines):
    print('\n'.join([''.join(line) for line in mapLines]))

# Calculate the password given our current position and the direction we are facing
def calculatePassword(currentPos, facing):
    return (1000 * (currentPos[0] + 1)) + (4 * (currentPos[1] + 1)) + directions.index(facing)

# Given a string, find the index of the first character that is not whitespace
# Used for Pt. 1 wrapping
def findIndexOfFirstNonWhitespace(string):
    for i in range(len(string)):
        if not string[i].isspace():
            return i
    return None

# Given a string, find the index of the last character that is not whitespace
# Used for Pt. 1 wrapping
def findIndexOfLastNonWhitespace(string):
    for i in range(len(string) - 1, -1, -1):
        if not string[i].isspace():
            return i
    return None

# Hard-coded based on my input. Divided input into 4x3 sections and assigned each of the faces a number
# Determines which face number we are on based on our current position
def getFace(currentPos):
    faces = {
        (0, 1): 1,
        (0, 2): 2,
        (1, 1): 3,
        (2, 1): 4,
        (2, 0): 5,
        (3, 0): 6
    }
    return faces[((currentPos[0] // 50), currentPos[1] // 50)]

# Going from one face to another of the cube...
# Used for Pt. 2 wrapping
def traverseFaces(currentPos, facing):

    # The top-left corners of each of the faces, hard-coded
    corners = {
        1: [0, 50],
        2: [0, 100],
        3: [50, 50],
        4: [100, 50],
        5: [100, 0],
        6: [150, 0]
    }

    # Also hard-coded based on the input. When going off of a face in a given direction, which face do we end up on, and which direction are we facing?
    traversals = {
        (1, '<'): (5, '>'),
        (1, '^'): (6, '>'),
        (2, '^'): (6, '^'),
        (2, '>'): (4, '<'),
        (2, 'v'): (3, '<'),
        (3, '<'): (5, 'v'),
        (3, '>'): (2, '^'),
        (4, '>'): (2, '<'),
        (4, 'v'): (6, '<'),
        (5, '^'): (3, '>'),
        (5, '<'): (1, '>'),
        (6, '<'): (1, 'v'),
        (6, 'v'): (2, 'v'),
        (6, '>'): (4, '^')
    }
    traversal = traversals[(getFace(currentPos), facing)]
    # If we end up going the opposite direction after moving faces, we need to reverse the offset on the new face
    #     .12      If we move off of 1 going left, we will end up on face 5 (heading right).
    #     .3.      If we move off near the top-left corner of 1, we will come in on the bottom-left corner of 5.
    #     54.      Since the corners we are tracking are the top left, we need to reverse the offset so that we're
    #     6..      counting from the bottom-left corner, not the top-left.
    traversalType = '-' if facing != traversal[1] and directions.index(facing) % 2 == directions.index(traversal[1]) % 2 else '+'
    offset = (currentPos[0] % 50) if facing in '<>' else (currentPos[1] % 50)
    newPos = corners[traversal[0]]
    if traversal[1] in '><':
        if traversal[1] == '<':
            newPos[1] += 49
        if traversalType == '+':
            newPos[0] += offset
        else:
            newPos[0] += 49 - offset
    elif traversal[1] in 'v^':
        if traversal[1] == '^':
            newPos[0] += 49
        if traversalType == '+':
            newPos[1] += offset
        else:
            newPos[1] += 49 - offset
    return newPos, traversal[1]

# Run through our instruction set
def runInstructions(mapLines, instructions, part1 = True):

    currentPos = [0, mapLines[0].index('.')]
    facing = '>'
    updateMap(mapLines, currentPos, facing)
    for instruction in instructions:
        # Movement instruction, go forward one step at a time
        if instruction.isdigit():
            for x in range(int(instruction)):
                originalPosition = currentPos[:]
                originalFacing = facing
                if facing == '>':
                    currentPos[1] += 1
                    if currentPos[1] >= width or mapLines[currentPos[0]][currentPos[1]].isspace():
                        if part1:
                            currentPos[1] = findIndexOfFirstNonWhitespace(mapLines[currentPos[0]])
                        else:
                            currentPos, facing = traverseFaces(originalPosition, facing)
                elif facing == '<':
                    currentPos[1] -= 1
                    if currentPos[1] < 0 or mapLines[currentPos[0]][currentPos[1]].isspace():
                        if part1:
                            currentPos[1] = findIndexOfLastNonWhitespace(mapLines[currentPos[0]])
                        else:
                            currentPos, facing = traverseFaces(originalPosition, facing)
                elif facing == 'v':
                    currentPos[0] += 1
                    if currentPos[0] >= height or mapLines[currentPos[0]][currentPos[1]].isspace():
                        if part1:
                            column = ''.join([mapLines[m][currentPos[1]] for m in range(height)])
                            currentPos[0] = findIndexOfFirstNonWhitespace(column)
                        else:
                            currentPos, facing = traverseFaces(originalPosition, facing)
                elif facing == '^':
                    currentPos[0] -= 1
                    if currentPos[0] < 0 or mapLines[currentPos[0]][currentPos[1]].isspace():
                        if part1:
                            column = ''.join([mapLines[m][currentPos[1]] for m in range(height)])
                            currentPos[0] = findIndexOfLastNonWhitespace(column)
                        else:
                            currentPos, facing = traverseFaces(originalPosition, facing)
                # We hit a wall, time to stop moving
                if mapLines[currentPos[0]][currentPos[1]] == '#':
                    currentPos = originalPosition[:]
                    facing = originalFacing
                    break
                updateMap(mapLines, currentPos, facing)
        # Rotation instruction, turn left or right
        else:
            facing = rotate(facing, instruction)
            updateMap(mapLines, currentPos, facing)
    #printMap(mapLines) # Uncomment to view a map of your journey
    password = calculatePassword(currentPos, facing)
    print("The password is", password)

# Pt. 1
runInstructions(mapLines.copy(), instructions)
# Pt. 2
runInstructions(mapLines.copy(), instructions, False)