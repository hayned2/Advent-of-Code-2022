import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day8_input1.txt')

# This is a 2-dimension array of tree heights, the input
treeGrid = []

# This is a 2-dimension array of whether a tree is visible or not
treeGridVisibility = {}

height = 0
for line in input1:
    line = line.strip()
    treeRow = [int(tree) for tree in line]
    treeGrid.append(treeRow)
    # All trees on the left and right edges are visible by default
    treeGridVisibility[height] = [True] + ([False] * (len(treeRow) - 2)) + [True]
    height += 1
# All trees on the top and bottom edges are visible by default
treeGridVisibility[0] = [True] * len(treeGrid[0])
treeGridVisibility[height - 1] = [True] * len(treeGrid[0])

input1.close()

# For part 2
bestScenicScore = 0
bestScenicScorePosition = None

# Go through the trees and check visibility from the top and left sides
currentColumnMaxes = treeGrid[0]
for x in range(1, len(treeGrid) - 1):
    currentRowMax = treeGrid[x][0]
    for y in range(1, len(treeGrid[x]) - 1):
        # Can be seen from the left
        if treeGrid[x][y] > currentRowMax:
            treeGridVisibility[x][y] = True
            currentRowMax = treeGrid[x][y]
        # Can be seen from the top
        if treeGrid[x][y] > currentColumnMaxes[y]:
            treeGridVisibility[x][y] = True
            currentColumnMaxes[y] = treeGrid[x][y]

        # Part 2, calculate the scenic scores from all 4 directions for the tree
        leftScenicScore = 0
        for tree in reversed(treeGrid[x][:y]):
            leftScenicScore += 1
            if tree >= treeGrid[x][y]:
                break
        rightScenicScore = 0
        for tree in treeGrid[x][y + 1:]:
            rightScenicScore += 1
            if tree >= treeGrid[x][y]:
                break
        topScenicScore = 0
        for tree in reversed([row[y] for row in treeGrid[:x]]):
            topScenicScore += 1
            if tree >= treeGrid[x][y]:
                break
        bottomScenicScore = 0
        for tree in [row[y] for row in treeGrid[x + 1:]]:
            bottomScenicScore += 1
            if tree >= treeGrid[x][y]:
                break
        totalScenicScore = leftScenicScore * rightScenicScore * topScenicScore * bottomScenicScore
        if totalScenicScore > bestScenicScore:
            bestScenicScore = totalScenicScore
            bestScenicScorePosition = (x, y)

# Go through the trees and check visibility from the bottom and right sides
currentColumnMaxes = treeGrid[-1]
for x in range(len(treeGrid) - 2, 0, -1):
    currentRowMax = treeGrid[x][-1]
    for y in range(len(treeGrid[x]) - 2, 0, -1):
        # Can be seen from the right
        if treeGrid[x][y] > currentRowMax:
            treeGridVisibility[x][y] = True
            currentRowMax = treeGrid[x][y]
        # Can be seen from the bottom
        if treeGrid[x][y] > currentColumnMaxes[y]:
            treeGridVisibility[x][y] = True
            currentColumnMaxes[y] = treeGrid[x][y]

# Calculate total number of Trues in the treeGridVisibility 2-D Array
visibleTrees = sum([sum([1 for tree in row if tree == True]) for row in treeGridVisibility.values()])

print("There are a total of", visibleTrees, "trees visible from outside of the grid")
print("The tree with the best scenic score is in position", bestScenicScorePosition, "with a score of", bestScenicScore)
        
