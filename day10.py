import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day10_input1.txt')

current_cycle = 0
x = 1
line = None
interestingSignals = 0
image = []
row = []

while current_cycle < 240:    

    # Increment the next cycle
    current_cycle += 1
    subCycle = current_cycle % 40

    # Part 2 - Determine if the sprite is currently visible on the pixel being rendered
    currentPixel = subCycle - 1 + (40 if subCycle == 0 else 0)
    if currentPixel in range(x - 1, x + 2):
        row.append('#')
    else:
        row.append('.')

    # Part 1 - Check if we are on an interesting cycle (midway through a subcycle), calculate the current signal strength
    if subCycle == 20:
        interestingSignals += current_cycle * x

    # Part 2 - If we have finished a subcycle, start rendering the next row of pixels
    elif subCycle == 0:
        print(current_cycle, subCycle, x)
        image.append(row)
        row = []

    # If we are not currently executing an instruction, get a new one
    if line == None:
        line = next(input1).strip().split()

        # If the instruction is a no-op, reset so we can grab a new instruction next cycle
        if line[0] == 'noop':
            line = None

    # In this branch, we are still executing an addx instruction from the previous cycle. Time to finish executing and reset
    else:
        x += int(line[1])
        line = None

input1.close()
print("The sum of the signal strengths is", interestingSignals)
print('\n'.join([''.join(row) for row in image]))
exit()