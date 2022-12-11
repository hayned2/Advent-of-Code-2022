import os
import math

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day11_input1.txt')

class Monkey:
    def __init__(self, id, startingItems, operation, test, trueTarget, falseTarget, reduceWorry):
        self.id = id
        self.items = startingItems[:]
        self.operation = operation
        self.test = test
        self.trueTarget = trueTarget
        self.falseTarget = falseTarget
        self.reduceWorry = reduceWorry
        self.inspections = 0
    
    def takeTurn(self, monkeys, GCM = 1):
        for x in range(len(self.items)):
            old = self.items[x]
            self.items[x] = eval(self.operation)
            if self.reduceWorry:
                self.items[x] = self.items[x] // 3
            else:
                self.items[x] %= GCM
            if self.items[x] % self.test == 0:
                monkeys[self.trueTarget].items.append(self.items[x])
            else:
                monkeys[self.falseTarget].items.append(self.items[x])
            self.inspections += 1
        self.items = []

instructions = input1.readlines()
input1.close()
x = 0
monkeys = []
monkeys2 = []
GCM = 1
while x < len(instructions):
    monkeyId = int(instructions[x].strip().split()[1][-2])
    startingItems = [int(num) for num in instructions[x + 1].strip().split(': ')[-1].split(',')]
    operation = instructions[x + 2].strip().split(' = ')[-1]
    test = int(instructions[x + 3].strip().split()[-1])
    GCM *= test
    trueTarget = int(instructions[x + 4].strip()[-1])
    falseTarget = int(instructions[x + 5].strip()[-1])
    monkeys.append(Monkey(monkeyId, startingItems, operation, test, trueTarget, falseTarget, True))
    monkeys2.append(Monkey(monkeyId, startingItems, operation, test, trueTarget, falseTarget, False))
    x += 7

for x in range(20):
    for monkey in monkeys:
        monkey.takeTurn(monkeys)
monkeyBusiness = math.prod(sorted([monkey.inspections for monkey in monkeys])[-2:])
print("The monkey business score in scenario #1 is", monkeyBusiness)

for x in range(10000):
    for monkey in monkeys2:
        monkey.takeTurn(monkeys2, GCM)
monkeyBusiness = math.prod(sorted([monkey.inspections for monkey in monkeys2])[-2:])
print("The monkey business score in scenario #2 is", monkeyBusiness)

exit()