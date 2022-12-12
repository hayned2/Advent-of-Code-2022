import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day12_input1.txt')
map = [line.strip() for line in input1.readlines()]
input1.close()

class Node:
    def __init__(self, row, column, height, parent = None, goal = None):
        self.row = row
        self.column = column
        if height == 'S':
            self.height = 1
        elif height == 'E':
            self.height = 27
        else:
            self.height = ord(height) - 96
        self.parent = parent

    def canTravelTo(self, otherHeight):
        if otherHeight == 'S':
            return True
        elif otherHeight == 'E':
            return self.height == 26
        return ord(otherHeight) - 96 <= self.height + 1

height = len(map)
width = len(map[0])

openNodes = []
openNodes2 = []
endNode = None

for y in range(len(map)):
    for x in range(len(map[y])):
        if map[y][x] == 'S' or map[y][x] == 'a':
            openNodes2.append(Node(y, x, map[y][x]))
        if map[y][x] == 'S':
            openNodes.append(Node(y, x, map[y][x]))
        if map[y][x] == 'E':
            endNode = Node(y, x, map[y][x])

def findShortestPath(openNodes, endNode):
    closedNodes = set()
    while len(openNodes) > 0:
        currentNode = openNodes.pop(0)
        closedNodes.add((currentNode.row, currentNode.column))
        if currentNode.height == 27:
            length = 0
            path = []
            while currentNode.parent != None:
                length += 1
                path.append(currentNode.height)
                currentNode = currentNode.parent
            return length
        else:
            neighbors = []
            if currentNode.row + 1 < height and currentNode.canTravelTo(map[currentNode.row + 1][currentNode.column]):
                neighbors.append(Node(currentNode.row + 1, currentNode.column, map[currentNode.row + 1][currentNode.column], currentNode, endNode))
            if currentNode.row - 1 >= 0 and currentNode.canTravelTo(map[currentNode.row - 1][currentNode.column]):
                neighbors.append(Node(currentNode.row - 1, currentNode.column, map[currentNode.row - 1][currentNode.column], currentNode, endNode))
            if currentNode.column + 1 < width and currentNode.canTravelTo(map[currentNode.row][currentNode.column + 1]):
                neighbors.append(Node(currentNode.row, currentNode.column + 1, map[currentNode.row][currentNode.column + 1], currentNode, endNode))
            if currentNode.column - 1 >= 0 and currentNode.canTravelTo(map[currentNode.row][currentNode.column - 1]):
                neighbors.append(Node(currentNode.row, currentNode.column - 1, map[currentNode.row][currentNode.column - 1], currentNode, endNode))
            for neighbor in neighbors:
                skip = False
                for node in openNodes:
                    if neighbor.column == node.column and neighbor.row == node.row:
                        skip = True
                        break
                if (neighbor.row, neighbor.column) in closedNodes:
                    skip = True
                if not skip:
                    openNodes.append(neighbor)
    return float('inf')

print("Starting at 'S', the shortest path is", findShortestPath(openNodes, endNode))
minPath = float('inf')
for startingNode in openNodes2:
    minPath = min(minPath, findShortestPath([startingNode], endNode))
print("Starting at either 'S' or any 'a', the shortest path is", minPath)