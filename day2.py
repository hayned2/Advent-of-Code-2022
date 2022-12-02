import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day2_input1.txt')

class Choice:

    RockPaperScissors = None

    def __init__(self, value, other = None):
        if not other:
            if value == 'A' or value == 'X':
                self.RockPaperScissors = 'Rock'
            elif value == 'B' or value == 'Y':
                self.RockPaperScissors = 'Paper'
            elif value == 'C' or value == 'Z':
                self.RockPaperScissors = 'Scissors'
        else:
            if value == 'X':
                if other == 'A':
                    self.RockPaperScissors = 'Scissors'
                elif other == 'B':
                    self.RockPaperScissors = 'Rock'
                elif other == 'C':
                    self.RockPaperScissors = 'Paper'
            elif value == 'Y':
                self.RockPaperScissors = Choice(other).RockPaperScissors
            elif value == 'Z':
                if other == 'A':
                    self.RockPaperScissors = 'Paper'
                elif other == 'B':
                    self.RockPaperScissors = 'Scissors'
                elif other == 'C':
                    self.RockPaperScissors = 'Rock'
    
    def result(self, other):
        if self.RockPaperScissors == other.RockPaperScissors:
            return 3
        if self.RockPaperScissors == 'Rock' and other.RockPaperScissors == 'Paper' \
            or self.RockPaperScissors == 'Paper' and other.RockPaperScissors == 'Scissors' \
            or self.RockPaperScissors == 'Scissors' and other.RockPaperScissors == 'Rock':
                return 0
        return 6
    
    def value(self):
        if self.RockPaperScissors == 'Rock':
            return 1
        elif self.RockPaperScissors == 'Paper':
            return 2
        elif self.RockPaperScissors == 'Scissors':
            return 3


score = 0
score2 = 0
for line in input1:
    line = line.split()
    opponent = Choice(line[0])
    you = Choice(line[1])
    you2 = Choice(line[1], line[0])
    score += you.result(opponent) + you.value()
    score2 += you2.result(opponent) + you2.value()
print("Your final total score is", score)
print("Your second final score is", score2)
