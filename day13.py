import os
import json
import copy

input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day13_input1.txt')
packets = [json.loads(line.strip()) for line in input1.readlines() if len(line.strip()) > 0]
input1.close()

class Packet:
    def __init__(self, packet):
        self.packet = packet
    def __lt__(self, other):
        return comparePackets(copy.deepcopy(self.packet), copy.deepcopy(other.packet))

def comparePackets(packet1, packet2):
    if len(packet1) > 0 and len(packet2) > 0:
        item1 = packet1[0]
        item2 = packet2[0]
        if type(item1) == int and type(item2) == int:
            if item1 == item2:
                return comparePackets(packet1[1:], packet2[1:])
            else:
                return item1 < item2
        elif type(item1) == list and type(item2) == list:
            result = comparePackets(item1, item2)
            if result != None:
                return result
            else:
                return comparePackets(packet1[1:], packet2[1:])
        elif type(item1) == int:
            packet1[0] = [packet1[0]]
            return comparePackets(packet1, packet2)
        else:
            packet2[0] = [packet2[0]]
            return comparePackets(packet1, packet2)
    elif len(packet1) == 0 and len(packet2) > 0:
        return True
    elif len(packet1) > 0 and len(packet2) == 0:
        return False
    else:
        return None

packetCounter = 0
pairCounter = 1
correctPairSum = 0
while packetCounter < len(packets):
    packet1 = packets[packetCounter]
    packet2 = packets[packetCounter + 1]
    if packet1 == None or packet2 == None:
        break
    if comparePackets(packet1, packet2):
        correctPairSum += pairCounter
    pairCounter += 1
    packetCounter += 2

print('The sum of the correctly-ordered pair indices is', correctPairSum)

packets.append([[2]])
packets.append([[6]])
packets = [Packet(packet) for packet in packets]
packets.sort()

decoderKey = 1
for x in range(len(packets)):
    if packets[x].packet == [[2]]:
        decoderKey *= (x + 1)
    elif packets[x].packet == [[6]]:
        decoderKey *= (x + 1)
        break

print("The decoder key is", decoderKey)
exit()