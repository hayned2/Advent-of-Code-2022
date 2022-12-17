# Credit to Dave A. Russell (https://github.com/davearussell) for the assistance in understanding a competent solution to this problem.

import os
import re

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day16_input1.txt')

# Class for the valves
class Valve:
    def __init__(self, flowRate, connectedValves, index):
        self.flowRate = flowRate
        self.connectedValves = {valve: 1 for valve in connectedValves}
        self.isOpen = False
        self.index = index

# Parse the input. Track the valves that have a flow rate and the starting valve in particular
valves = {}
valvesOfInterest = set()
indexToValve = {}
for line in input1:
    line = line.strip().split()
    valveLabel = line[1]
    valveFlowRate = int(re.findall(r'-?\d+', line[4])[0])
    connectedValves = [label.replace(',', '') for label in line[9:]]
    valves[valveLabel] = Valve(valveFlowRate, connectedValves, len(valvesOfInterest) + 1 if valveFlowRate > 0 else None)
    if valveFlowRate > 0:
        valvesOfInterest.add(valveLabel)
        indexToValve[valves[valveLabel].index] = valveLabel
input1.close()
valves['AA'].index = 0
valvesOfInterest.add('AA')
indexToValve[0] = 'AA'

# Remove the valves that have no flow rate, connect their neighbors with costs higher than 1
for valve in valves:
    if valve not in valvesOfInterest:
        for neighbor in valves[valve].connectedValves:
            for neighbor2 in valves[valve].connectedValves:
                if valve in valves[neighbor].connectedValves and neighbor != neighbor2:
                    if neighbor2 not in valves[neighbor].connectedValves or valves[neighbor].connectedValves[neighbor2] > valves[valve].connectedValves[neighbor2] + valves[valve].connectedValves[neighbor]:
                        valves[neighbor].connectedValves[neighbor2] = valves[valve].connectedValves[neighbor2] + valves[valve].connectedValves[neighbor]
                    if neighbor not in valves[neighbor2].connectedValves or valves[neighbor2].connectedValves[neighbor] > valves[valve].connectedValves[neighbor] + valves[valve].connectedValves[neighbor2]:
                        valves[neighbor2].connectedValves[neighbor] = valves[valve].connectedValves[neighbor] + valves[valve].connectedValves[neighbor2]
                    del valves[neighbor].connectedValves[valve]
                    del valves[neighbor2].connectedValves[valve]
valves = {key:val for key, val in valves.items() if key in valvesOfInterest}

# Warshall-Floyd algorithm to calculate the shortest paths from each vertex to every other vertex
distances = [[float('inf')] * len(valvesOfInterest) for _ in range(len(valvesOfInterest))]
for x in range(len(distances)):
    distances[x][x] = 0
for valve in valvesOfInterest:
    for neighbor in valves[valve].connectedValves:
        distances[valves[valve].index][valves[neighbor].index] = valves[valve].connectedValves[neighbor]
        distances[valves[neighbor].index][valves[valve].index] = valves[valve].connectedValves[neighbor]
for k in range(len(valvesOfInterest)):
    for i in range(len(valvesOfInterest)):
        for j in range(len(valvesOfInterest)):
            distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

# Update the class objects to store the distances to every other valve
for i in range(len(distances)):
    for j in range(len(distances)):
        if i != j:
            valves[indexToValve[i]].connectedValves[indexToValve[j]] = distances[i][j]

# Calculate every possible path that can be traversed in the time limit
def findAllPaths(currentValve, unvisitedValves, visitedValves, timeLeft):
    for neighbor in unvisitedValves:
        timeToVisit = valves[currentValve].connectedValves[neighbor] + 1
        if timeToVisit < timeLeft:
            yield from findAllPaths(neighbor, unvisitedValves - {neighbor}, visitedValves + [neighbor], timeLeft - timeToVisit)
    yield visitedValves

# Calculate the value of a given path
def calculatePath(startingValve, path, timeLeft):
    pressureReleased = 0
    currentValve = startingValve
    for neighbor in path:
        timeToVisit = valves[currentValve].connectedValves[neighbor] + 1
        timeLeft -= timeToVisit
        pressureReleased += timeLeft * valves[neighbor].flowRate
        currentValve = neighbor
    return pressureReleased

# Part 1 - Find all paths that can be traversed from 'AA' within 30 minutes, find the one with the best score
allPaths = findAllPaths('AA', valvesOfInterest - {'AA'}, [], 30)
bestPressure = max([calculatePath('AA', path, 30) for path in allPaths])
print("By myself, I can release a total of", bestPressure, "in 30 minutes")

# Part 2- Find all the paths that can be traversed from 'AA' within 26 minutes
allPaths = findAllPaths('AA', valvesOfInterest - {'AA'}, [], 26)

# Calculate the scores of each path, and pair them with the paths themselves. Sort from highest to lowest scores
pressures = [(calculatePath('AA', path, 26), set(path)) for path in allPaths]
pressures.sort()
pressures.reverse()

# Find two sets of paths with the highest scores that are completely disjointed
bestPressure = 0
for x, (score1, path1) in enumerate(pressures):
    # If the current score cannot possibly be better than our best one (since all scores it can be combined with are <= this one), we're done
    if score1 * 2 < bestPressure:
        break
    # Check every path result after this one for the highest-scoring disjointed path
    for score2, path2 in pressures[x+1:]:
        # If the sets are disjointed, this is the highest scoring one
        if not path1 & path2:
            score = score1 + score2
            if score > bestPressure:
                bestPressure = score
            break
print("With my elephant pal, we can release a total of", bestPressure, "in 26 minutes")
exit()