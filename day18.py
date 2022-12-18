import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day18_input1.txt')

cubes = set()
minx = float('inf')
maxx = -float('inf')
miny = float('inf')
maxy = -float('inf')
minz = float('inf')
maxz = -float('inf')
for line in input1:
    line = line.strip().split(",")
    x = int(line[0])
    y = int(line[1])
    z = int(line[2])
    minx = min(minx, x)
    maxx = max(maxx, x)
    miny = min(miny, y)
    maxy = max(maxy, y)
    minz = min(minz, z)
    maxz = max(maxz, z)
    cubes.add((x, y, z))
input1.close()

# For each face of a cube, check to see if there is a cube against it
exposedSides = 0
for cube in cubes:
    if (cube[0] + 1, cube[1], cube[2]) not in cubes:
        exposedSides += 1
    if (cube[0] - 1, cube[1], cube[2]) not in cubes:
        exposedSides +=1
    if (cube[0], cube[1] + 1, cube[2]) not in cubes:
        exposedSides += 1
    if (cube[0], cube[1] - 1, cube[2]) not in cubes:
        exposedSides += 1
    if (cube[0], cube[1], cube[2] + 1) not in cubes:
        exposedSides += 1
    if (cube[0], cube[1], cube[2] - 1) not in cubes:
        exposedSides += 1
print("There are", exposedSides, "exposed sides in total")

steamCubes = set()
queue = set()
queue.add((minx, miny, minz))
exteriorSides = 0
minx -= 1
maxx += 1
miny -= 1
maxy += 1
minz -= 1
maxz += 1
# Create a steam cube in the corner, and expand as far as it can within a 1-cube-padded area around the whole shape, counting exposed faces
while len(queue) > 0:

    currentPos = queue.pop()

    downX = (currentPos[0] - 1, currentPos[1], currentPos[2])
    if downX[0] >= minx and downX not in steamCubes:
        if downX in cubes:
            exteriorSides += 1
        else:
            queue.add(downX)

    upX = (currentPos[0] + 1, currentPos[1], currentPos[2])
    if upX[0] <= maxx and upX not in steamCubes:
        if upX in cubes:
            exteriorSides += 1
        else:
            queue.add(upX)

    downY = (currentPos[0], currentPos[1] - 1, currentPos[2])
    if downY[1] >= miny and downY not in steamCubes:
        if downY in cubes:
            exteriorSides += 1
        else:
            queue.add(downY)

    upY = (currentPos[0], currentPos[1] + 1, currentPos[2])
    if upY[1] <= maxy and upY not in steamCubes:
        if upY in cubes:
            exteriorSides += 1
        else:
            queue.add(upY)

    downZ = (currentPos[0], currentPos[1], currentPos[2] - 1)
    if downZ[2] >= minz and downZ not in steamCubes:
        if downZ in cubes:
            exteriorSides += 1
        else:
            queue.add(downZ)

    upZ = (currentPos[0], currentPos[1], currentPos[2] + 1)
    if upZ[2] <= maxz and upZ not in steamCubes:
        if upZ in cubes:
            exteriorSides += 1
        else:
            queue.add(upZ)

    steamCubes.add(currentPos)
print("There are", exteriorSides, "exterior sides")
exit()