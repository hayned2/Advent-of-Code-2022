import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day9_input1.txt')

def moveHead(direction, headPosition):
    if direction == 'U':
        headPosition[1] += 1
    elif direction == 'D':
        headPosition[1] -= 1
    elif direction == 'L':
        headPosition[0] -= 1
    else:
        headPosition[0] += 1

def followKnot(leader, follower):
    if abs(leader[0] - follower[0]) > 1 or abs(leader[1] - follower[1]) > 1:
        if leader[0] > follower[0]:
            follower[0] += 1
        elif leader[0] < follower[0]:
            follower[0] -= 1
        if leader[1] > follower[1]:
            follower[1] += 1
        elif leader[1] < follower[1]:
            follower[1] -= 1

visitedPositions2Knot = set()
visitedPositions10Knot = set()
knots = 10
ropeChain = [[0, 0] for _ in range(knots)]

for line in input1:
    line = line.strip()
    [direction, distance] = line.split()
    distance = int(distance)
    for x in range(distance):
        moveHead(direction, ropeChain[0])
        for y in range(len(ropeChain) - 1):
            followKnot(ropeChain[y], ropeChain[y + 1])
        visitedPositions2Knot.add(tuple(ropeChain[1]))
        visitedPositions10Knot.add(tuple(ropeChain[-1]))

input1.close()

print("The tail of the 2-knot rope visited a total of", len(visitedPositions2Knot), "locations")
print("The tail of the 10-knot rope visited a total of", len(visitedPositions10Knot), "locations")

exit()