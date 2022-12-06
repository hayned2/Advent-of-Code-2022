import os

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day6_input1.txt')

counter = 0
counter2 = 0
buffer = []
buffer2 = []
packetFound = False
line = next(input1)
for character in line:
    
    # Part 1 - Stop looking for this once we find the first unique set of 4 characters
    if not packetFound:
        counter += 1
        buffer.append(character)
        if len(buffer) > 4:
            buffer = buffer[1:]
        if len(buffer) == 4 and len(buffer) == len(set(buffer)):
            print("Starting packet found at position", counter)
            packetFound = True

    # Part 2 - Keep going until we find the first unique set of 14 characters
    counter2 += 1
    buffer2.append(character)
    if len(buffer2) > 14:
        buffer2 = buffer2[1:]
    if len(buffer2) == 14 and len(buffer2) == len(set(buffer2)):
        print("Message packet found at position", counter2)
        break

input1.close()
exit()  