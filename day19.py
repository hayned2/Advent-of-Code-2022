import os
import re
import multiprocessing as mp
blueprints = {}
bp = 1
input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day19_input1.txt')
for line in input1:
    line = line.strip()
    values = [int(value) for value in re.findall('\d+', line)]
    blueprints[bp] = {}
    blueprints[bp]['OR-Ore'] = values[1]
    blueprints[bp]['CR-Ore'] = values[2]
    blueprints[bp]['OB-Ore'] = values[3]
    blueprints[bp]['OB-Clay'] = values[4]
    blueprints[bp]['GR-Ore'] = values[5]
    blueprints[bp]['GR-Obs'] = values[6]
    bp += 1
input1.close()

def runBlueprint(blueprint, timeLeft, robots, resources, skippedRobots):

    # Time's run out
    if timeLeft == 0:
        return resources['geode']
    
    # Calculate how many resources gained at the end of the minute
    newResources = resources.copy()
    newResources['ore'] += robots['ore']
    newResources['clay'] += robots['clay']
    newResources['obsidian'] += robots['obsidian']
    newResources['geode'] += robots['geode']

    mostGeodes = newResources['geode']

    # Create new robots? Only do so if we have the resources to, and it makes sense to.
    # (If we can never spend more than x ore in a round, there is no point in having more than x ore robots, for example)
    mostOreNeeded = max(blueprint['OR-Ore'], blueprint['CR-Ore'], blueprint['OB-Ore'], blueprint['GR-Ore'])
    couldBuildOreRobot = robots['ore'] < mostOreNeeded and resources['ore'] >= blueprint['OR-Ore']
    couldBuildClayRobot = robots['clay'] < blueprint['OB-Clay'] and resources['ore'] >= blueprint['CR-Ore']
    couldBuildObsidianRobot = robots['obsidian'] < blueprint['GR-Obs'] and resources['ore'] >= blueprint['OB-Ore'] and resources['clay'] >= blueprint['OB-Clay']
    couldBuildGeodeRobot = resources['ore'] >= blueprint['GR-Ore'] and resources['obsidian'] >= blueprint['GR-Obs']

    # Always build a geode robot if we can
    if couldBuildGeodeRobot:
        newResources2 = newResources.copy()
        newResources2['ore'] -= blueprint['GR-Ore']
        newResources2['obsidian'] -= blueprint['GR-Obs']
        newRobots = robots.copy()
        newRobots['geode'] += 1
        return runBlueprint(blueprint, timeLeft - 1, newRobots, newResources2, set())

    # Attempt to build any of the other 3 robots if we can't make a geode robot
    if couldBuildOreRobot and 'ore' not in skippedRobots:
        newResources2 = newResources.copy()
        newResources2['ore'] -= blueprint['OR-Ore']
        newRobots = robots.copy()
        newRobots['ore'] += 1
        mostGeodes = max(mostGeodes, runBlueprint(blueprint, timeLeft - 1, newRobots, newResources2, set()))
    if couldBuildClayRobot and 'clay' not in skippedRobots:
        newResources2 = newResources.copy()
        newResources2['ore'] -= blueprint['CR-Ore']
        newRobots = robots.copy()
        newRobots['clay'] += 1
        mostGeodes = max(mostGeodes, runBlueprint(blueprint, timeLeft - 1, newRobots, newResources2, set()))
    if couldBuildObsidianRobot and 'obsidian' not in skippedRobots:
        newResources2 = newResources.copy()
        newResources2['ore'] -= blueprint['OB-Ore']
        newResources2['clay'] -= blueprint['OB-Clay']
        newRobots = robots.copy()
        newRobots['obsidian'] += 1
        mostGeodes = max(mostGeodes, runBlueprint(blueprint, timeLeft - 1, newRobots, newResources2, set()))

    # If we skipped building a robot when we could, prevent that robot from being built until a different robot is built
    if couldBuildOreRobot:
        skippedRobots.add('ore')
    if couldBuildClayRobot:
        skippedRobots.add('clay')
    if couldBuildObsidianRobot:
        skippedRobots.add('obsidian')
    return max(mostGeodes, runBlueprint(blueprint, timeLeft - 1, robots, newResources, skippedRobots))

if __name__ == '__main__':

    # Part 1
    qualityScores = 0
    for blueprintNumber in blueprints:
        geodes = runBlueprint(blueprints[blueprintNumber], 24, {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}, {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}, set())
        print("Blueprint number", blueprintNumber, "can crack a maximum of", geodes, "geodes in 24 minutes for a quality score of", geodes * blueprintNumber)
        qualityScores += geodes * blueprintNumber
    print("The sum of all blueprint quality scores is", qualityScores)

    # Part 2
    geodeValue = 1
    for blueprintNumber in range(1, 4):
        geodes = runBlueprint(blueprints[blueprintNumber], 32, {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}, {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}, set())
        print("Blueprint", blueprintNumber, "can crack a maximum of", geodes, "geodes in 32 minutes")
        geodeValue *= geodes
    print("The product of the 3 remaining blueprint geode amounts is", geodeValue)
    exit()