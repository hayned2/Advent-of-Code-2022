import os
import re

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day15_input1.txt')

class Sensor:
    def __init__(self, x, y, closestBeacon):
        self.x = x
        self.y = y
        self.distance = abs(closestBeacon[0] - x) + abs(closestBeacon[1] - y)

    def withinDistance(self, other):
        distance = abs(self.x - other[0]) + abs(self.y - other[1])
        return distance <= self.distance and distance != 0

    def getCoverageOnRow(self, row):
        span = self.distance - abs(self.y - row)
        if span > 0:
            return [self.x - span, self.x + span]
        return None

sensors = []
minX = float('inf')
maxX = -float('inf')

for line in input1:
    [sensorx, sensory, beaconx, beacony] = [int(num) for num in re.findall(r'-?\d+', line)]
    sensor = Sensor(sensorx, sensory, (beaconx, beacony))
    sensors.append(sensor)
    minX = min(minX, sensorx, beaconx)
    maxX = max(maxX, sensorx, beaconx)
input1.close()

# Part 1
def getCoverageOnRowForAllSensors(desiredRow, limitMinX = None, limitMaxX = None):
    beaconCoverage = []
    for sensor in sensors:
        coverage = sensor.getCoverageOnRow(desiredRow)
        if coverage != None:
            if limitMinX != None and limitMaxX != None:
                if coverage[0] > limitMaxX or limitMinX > coverage[1]:
                    continue
                coverage[0] = max(limitMinX, coverage[0])
                coverage[1] = min(limitMaxX, coverage[1])
            beaconCoverage.append(coverage)
    beaconCoverage.sort()
    stack = []
    stack.append(beaconCoverage[0])
    for x in beaconCoverage[1:]:
        if stack[-1][0] <= x[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], x[-1])
        else:
            stack.append(x)
    return stack

desiredRow = 2000000
beaconCoverage = getCoverageOnRowForAllSensors(desiredRow)
beaconFreeSpots = 0
for interval in beaconCoverage:
    beaconFreeSpots += interval[1] - interval[0]
print("There are a total of", beaconFreeSpots, "beacon-free positions on row", desiredRow)

# Part 2
for row in range(4000000):
    coverage = getCoverageOnRowForAllSensors(row, 0, 4000000)
    if coverage[0][1] - coverage[0][0] != 4000000:
        print("The tuning frequency is", ((coverage[0][1] + 1) * 4000000) + row)
        break

exit()