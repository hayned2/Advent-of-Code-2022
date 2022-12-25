import os

def SNAFU_To_Decimal(number):
    value = 0
    place = 0
    for digit in reversed(number):
        if digit == '-':
            digit = -1
        elif digit == '=':
            digit = -2
        value += (5 ** (place)) * int(digit)
        place += 1
    return value

def Decimal_To_SNAFU(number):
    if number > 0:
        divisor = (number + 2) // 5
        remainder = (number + 2) % 5
        return Decimal_To_SNAFU(divisor) + '=-012'[remainder]
    else:
        return ''

number = 0
input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day25_input1.txt')
for line in input1:
    line = line.strip()
    number += SNAFU_To_Decimal(line)
input1.close()

print("The SNAFU number to input is", Decimal_To_SNAFU(number))