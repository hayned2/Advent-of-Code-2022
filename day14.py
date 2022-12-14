import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day14_input1.txt')
rocks = [line.strip() for line in input1.readlines()]
input1.close()

minX = float('inf')
minY = 0
maxX = -float('inf')
maxY = -float('inf')
rocks = [rockline.split(' -> ') for rockline in rocks]
for rockline in rocks:
    for r in range(len(rockline)):
        rockline[r] = rockline[r].split(',')
        x = int(rockline[r][0])
        y = int(rockline[r][1])
        minX = min(x, minX)
        maxX = max(x, maxX)
        maxY = max(y, maxY)
        rockline[r] = (x, y)

area = []
for y in range(maxY - minY + 1):
    area.append(['.'] * (maxX - minX + 1))
area[0][500 - minX] = '+'

for rockline in rocks:
    for r in range(len(rockline) - 1):
        if rockline[r][0] != rockline[r + 1][0]:
            start = min(rockline[r][0], rockline[r + 1][0]) - minX
            end = max(rockline[r][0], rockline[r + 1][0]) - minX
            for r2 in range(start, end + 1):
                area[rockline[r][1]][r2] = '#'
        elif rockline[r][1] != rockline[r + 1][1]:
            start = min(rockline[r][1], rockline[r + 1][1])
            end = max(rockline[r][1], rockline[r + 1][1])
            for r2 in range(start, end + 1):
                area[r2][rockline[r][0] - minX] = '#'

area.append(['.'] * len(area[0]))
area.append(['#'] * len(area[0]))

sandCount = 0
spoutX = 500 - minX
part1 = True
while True:
    sandCount += 1
    sandPos = [0, spoutX]
    voided = False
    while True:
        sandPos[0] += 1
        if sandPos[0] > maxY:
            voided = True
        if area[sandPos[0]][sandPos[1]] != '.':
            newX = sandPos[1] - 1
            if newX < 0:
                voided = True
                for row in range(len(area) - 1):
                    area[row] = (['.'] * 2) + area[row]
                area[-1] = (['#'] * 2) + area[-1]
                sandPos[1] += 2
                newX += 2
                minX += 2
                spoutX += 2
            if area[sandPos[0]][newX] == '.':
                sandPos[1] = newX
            else:
                newX2 = sandPos[1] + 1
                if newX2 > (maxX - minX):
                    voided = True
                    for row in range(len(area) - 1):
                        area[row] += ['.'] * 2
                    area[-1] += ['#'] * 2
                if area[sandPos[0]][newX2] == '.':
                    sandPos[1] = newX2
                else:
                    sandPos[0] -= 1
                    area[sandPos[0]][sandPos[1]] = 'o'
                    break
    if voided and part1:
        print('\n'.join(''.join(row) for row in area))
        print("Sand #", sandCount, "fell into the void!")
        print(sandCount - 1, 'units of sand can fall and come to rest before sand starts flowing into the abyss')
        part1 = False
    if sandPos == [0, spoutX]:
        #print('\n'.join(''.join(row) for row in area))
        print("All filled up after", sandCount, "units of sand!")
        break   

exit()