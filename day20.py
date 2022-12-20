import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day20_input1.txt')

# Save the numbers as a tuple of their value and their original positions
# Mark down 0's original position
numbers = []
x = 0
zero = None
for line in input1:
    line = line.strip()
    numbers.append((int(line), x))
    x += 1
    if line == '0':
        zero = numbers[-1]
input1.close()

# Mix the numbers using Python list functions. 
# There's some funkiness with how to handle numbers at the beginning/end of the list.
# Since only relative positions matter in the end, tack everything questionable at the end instead of guessing
def mixNumbers(numbers, iterations):
    mixedNumbers = numbers.copy()
    for _ in range(iterations):
        for number in numbers:
            position = mixedNumbers.index(number)
            mixedNumbers.remove(number)
            position = (position + number[0]) % (len(numbers) - 1)
            if position == 0:
                position = len(numbers) - 1
            mixedNumbers.insert(position, number)
    return mixedNumbers

# Multiply all values in the numbers list by the decryption key
def applyDecryptionKey(numbers, decryptionKey):
    if decryptionKey == 1:
        return numbers.copy()
    return [(number[0] * decryptionKey, number[1]) for number in numbers]

# Mix the numbers, then calculate the coordinates based on the position of the zero value
def mixAndGetCoordinates(numbers, iterations, zero, decryptionKey = 1):
    numbers = applyDecryptionKey(numbers, decryptionKey)
    mixedNumbers = mixNumbers(numbers, iterations)
    zeroPosition = mixedNumbers.index(zero)
    OneThousand = (zeroPosition + 1000) % len(numbers)
    TwoThousand = (zeroPosition + 2000) % len(numbers)
    ThreeThousand = (zeroPosition + 3000) % len(numbers)
    print("The coordinate is", mixedNumbers[OneThousand][0] + mixedNumbers[TwoThousand][0] + mixedNumbers[ThreeThousand][0])

# Part 1
mixAndGetCoordinates(numbers, 1, zero)

# Part 2
decryptionKey = 811589153
mixAndGetCoordinates(numbers, 10, zero, decryptionKey)
exit()