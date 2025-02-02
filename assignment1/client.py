import sys
import json

filename = sys.argv[1]

class OccupancyTime:
    def __init__(self, startTime: int, endingTime: int):
        self.start = startTime
        self.end = endingTime

    def isDisjunctive(self, otherStart, otherEnd):
        if self.end < otherStart or self.start > otherEnd:
            return True
        return False

class Graph:
    def __init__(self,vertices):
        self.vertices = vertices


with open(filename, "r") as file:
    data = json.load(file)

possibleCircuits = data["possible-circuits"]

switchOccupancy = {}
for switch in data["switches"]:
    switchOccupancy[switch] = []

actionLog = []

for action in data["simulation"]["demands"]:
    startingPoint = action["end-points"][0]
    endingPoint = action["end-points"][1]
    startTime = int(action["start-time"])
    endTime = int(action["end-time"])
    routeFound = False
    for circuit in possibleCircuits:
        goodRoute = True
        if circuit[0] == startingPoint and circuit[-1] == endingPoint:
            for i in range(1, len(circuit) - 1):
                if len(switchOccupancy[circuit[i]]) != 0:
                    for occupiedFor in switchOccupancy[circuit[i]]:
                        if not occupiedFor.isDisjunctive(startTime, endTime):
                            goodRoute = False
                            break

            if not goodRoute:
                break
            else:
                for j in range(1, len(circuit) - 1):
                    switchOccupancy[circuit[j]].append(OccupancyTime(startTime, endTime))
                routeFound = True
                break
    if routeFound:
        actionLog.append(["igény foglalás:",f"{startingPoint}<->{endingPoint}","st:",startTime, "sikeres"])
        actionLog.append(["igény felszabadítás:", f"{startingPoint}<->{endingPoint}", "st:", endTime])
    else:
        actionLog.append(["igény foglalás:", f"{startingPoint}<->{endingPoint}", "st:", startTime, "sikertelen"])

actionLog.sort(key=lambda time: time[3])
for x in actionLog:
    print(' '.join(map(str, x)))

