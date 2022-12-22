import os
from sympy.solvers import solve
from sympy import Symbol, sympify

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day21_input2.txt')

# Parse the input, tracking monkeys we know the values of right off the first pass in knownMonkeys
# And monkeys that require some calculation / waiting in unknownMonkeys
knownMonkeys = {}
unknownMonkeys = {}
for line in input1:
    line = line.strip()
    line = line.split(": ")
    if line[1].isdigit():
        knownMonkeys[line[0]] = int(line[1])
    else:
        [monkey1, operation, monkey2] = line[1].split()
        if monkey1 in knownMonkeys and monkey2 in knownMonkeys:
            knownMonkeys[line[0]] = int(eval(str(knownMonkeys[monkey1]) + operation + str(knownMonkeys[monkey2])))
        else:
            unknownMonkeys[line[0]] = [monkey1, monkey2, operation]
input1.close()

# Copy the clean inputs for part 2
knownMonkeysPt2 = knownMonkeys.copy()
del knownMonkeysPt2['humn']
unknownMonkeysPt2 = unknownMonkeys.copy()

# Keep making passes through the unknownMonkeys until we find "root"'s true value
while len(unknownMonkeys) > 0 or 'root' not in knownMonkeys:
    foundMonkeys = set()
    for monkey in unknownMonkeys:
        [monkey1, monkey2, operation] = unknownMonkeys[monkey]
        if monkey1 in knownMonkeys and monkey2 in knownMonkeys:
            value = int(eval(str(knownMonkeys[monkey1]) + operation + str(knownMonkeys[monkey2])))
            foundMonkeys.add(monkey)
            knownMonkeys[monkey] = value
    for monkey in foundMonkeys:
        del unknownMonkeys[monkey]
print("The root monkey should yell the number", knownMonkeys['root'])

# Pt. 2, solve everything we can without knowing the human's value
while len(unknownMonkeysPt2) > 0:
    foundMonkeys = set()
    for monkey in unknownMonkeysPt2:
        [monkey1, monkey2, operation] = unknownMonkeysPt2[monkey]
        if monkey1 in knownMonkeysPt2 and monkey2 in knownMonkeysPt2:
            value = int(eval(str(knownMonkeysPt2[monkey1]) + operation + str(knownMonkeysPt2[monkey2])))
            foundMonkeys.add(monkey)
            knownMonkeysPt2[monkey] = value
    for monkey in foundMonkeys:
        del unknownMonkeysPt2[monkey]
    if len(foundMonkeys) == 0:
        break

# Expand a monkey's unknown values. So if monkey = m2 + m3, m2 = humn * 3, and m3 = 10 we will get monkey = '(humn * 3) + 10' (with more parentheses)
# This assumes no cycles and that 'humn' is the only unknown variable
def expandValue(monkey, knownMonkeys, unknownMonkeys):
    if monkey in knownMonkeys:
        return str(knownMonkeys[monkey])
    elif monkey != 'humn':
        [monkey1, monkey2, operation] = unknownMonkeys[monkey]
        return '(' + expandValue(monkey1, knownMonkeys, unknownMonkeys) + ')' + operation + '(' + expandValue(monkey2, knownMonkeys, unknownMonkeys) + ')'
    else:
        return monkey

# Turn the problem into a solveable algebraic expression with a single variable 'humn'
# Use sympy to solve the expression for the single variable
equation = sympify("Eq(" + expandValue(unknownMonkeysPt2['root'][0], knownMonkeysPt2, unknownMonkeysPt2) + '-' + expandValue(unknownMonkeysPt2['root'][1], knownMonkeysPt2, unknownMonkeysPt2) + ",0)")
humn = Symbol('humn')
print("The human should yell the number", solve(equation)[0])
exit()