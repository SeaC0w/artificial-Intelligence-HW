# by Kerim Celik and Julia Connelly for AI, 02/02/2018
import random
import numpy
import queue
import heapq


def onesInList(ls):
    ret = []
    for i in range(len(ls)):
        if ls[i] != 0:
            ret.append(i)
    return ret


def getListAverage(ls):
    return sum(ls) / len(ls)


def getListStdDev(ls):
    return numpy.std(ls)


def inRange(num, opt):
    return opt <= num < opt + 1


def getAdjustForOptAvg(avg, optAvg, numItems):
    return numItems * optAvg - avg * numItems


class Room:
    def __init__(self, temp, humid):
        self.temp = temp
        self.humid = humid
        
    def setTemp(self, value):
        self.temp = value
        
    def setHumid(self, value):
        self.humid = value

    def adjustTemp(self, value):
        self.temp += value

    def adjustHumid(self, value):
        self.humid += value

    def getOptDifference(self, optTemp, optHumid):
        return abs(optTemp - self.temp) + abs(optHumid - self.humid)

        
class Building:
    def __init__(self, edges):
        self.numRooms = 12
        self.minTemp = 65
        self.maxTemp = 75
        self.optTemp = 72
        self.minHumid = 45
        self.maxHumid = 55
        self.optHumid = 47
        self.tempStdDev = 1.75
        self.humidStdDev = 1.5

        self.roomList = []
        for i in range(self.numRooms):
            x = Room(random.randint(self.minTemp, self.maxTemp), random.randint(self.minHumid, self.maxHumid))
            self.roomList.append(x)

        self.edgeMatrix = []
        for i in range(self.numRooms):
            self.edgeMatrix.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        for e in edges:
            self.edgeMatrix[int(e[0]) - 1][int(e[1]) - 1] = int(e[2])
            self.edgeMatrix[int(e[1]) - 1][int(e[0]) - 1] = int(e[2])

    def display(self):
        # print("roomList len = " + str(len(self.roomList)))
        print("avg temp: " + str(self.getAvgTemp()))
        print("std dev temp: " + str(self.getStdDevTemp()))
        print("avg humid: " + str(self.getAvgHumid()))
        print("std dev humid: " + str(self.getStdDevHumid()))
        print("rooms: ")
        for index, room in enumerate(self.roomList):
            print("room: " + str(index + 1) + " temp: " + str(room.temp) + " humid: " + str(room.humid))

    def isOpt(self):
        avgTemp = self.getAvgTemp()
        avgHumid = self.getAvgHumid()
        stdDevTemp = self.getStdDevTemp()
        stdDevHumid = self.getStdDevHumid()
        avgTempGood = inRange(avgTemp, self.optTemp)
        avgHumidGood = inRange(avgHumid, self.optHumid)
        stdDevTempGood = stdDevTemp < self.tempStdDev + 0.1
        stdDevHumidGood = stdDevHumid < self.humidStdDev + 0.01
        return avgTempGood and stdDevTempGood and avgHumidGood and stdDevHumidGood

    def getMaxDifRoom(self):
        maxRoom = -1
        maxVal = 0
        for i, r in enumerate(self.roomList):
            dif = r.getOptDifference(self.optTemp, self.optHumid)
            if dif > maxVal:
                maxVal = dif
                maxRoom = i
        return maxRoom

    def getNeighbors(self, roomIndex):
        return onesInList(self.edgeMatrix[roomIndex])

    def getRandomRoom(self):
        return random.randint(0, self.numRooms - 1)

    def getAvgTemp(self):
        temps = map(lambda r: r.temp, self.roomList)
        return getListAverage(list(temps))

    def getAvgHumid(self):
        humids = map(lambda r: r.humid, self.roomList)
        return getListAverage(list(humids))

    def getStdDevTemp(self):
        temps = map(lambda r: r.temp, self.roomList)
        return getListStdDev(list(temps))

    def getStdDevHumid(self):
        humids = map(lambda r: r.humid, self.roomList)
        return getListStdDev(list(humids))

    def getEdge(self, roomA, roomB):
        return self.edgeMatrix[roomA][roomB]

    def setRoomOpt(self, room):
        self.roomList[room].setTemp(self.optTemp)
        self.roomList[room].setHumid(self.optHumid)

        # avgTemp = self.getAvgTemp()
        # avgHumid = self.getAvgHumid()
        # stdDevTemp = self.getStdDevTemp()
        # stdDevHumid = self.getStdDevHumid()
        # avgTempGood = inRange(avgTemp, self.optTemp)
        # avgHumidGood = inRange(avgHumid, self.optHumid)
        # stdDevTempGood = stdDevTemp < self.tempStdDev + 0.1
        # stdDevHumidGood = stdDevHumid < self.humidStdDev + 0.01
        # # if the temperature measures are not correct, change this room
        # if not (avgTempGood and stdDevTempGood):
        #     # if the std dev is in range, adjust room base on current avg
        #     if stdDevTempGood:
        #         # NOTE!!!!!!!!!! This will over adjust!!!!
        #         self.roomList[room].adjustTemp(getAdjustForOptAvg(avgTemp, self.optTemp, self.numRooms))
        #     # otherwise move temperature closer to desired average
        #     else:
        #         self.roomList[room].setTemp(self.optTemp)
        # # otherwise, change the humidity
        # elif not (avgHumidGood and stdDevHumidGood):
        #     # if the std dev is in range, adjust room base on current avg
        #     if stdDevHumidGood:
        #         # NOTE!!!!!!!!!! This will over adjust!!!!
        #         self.roomList[room].adjustHumid(getAdjustForOptAvg(avgHumid, self.optHumid, self.numRooms))
        #     # otherwise move humidity closer to desired average
        #     else:
        #         self.roomList[room].setHumid(self.optHumid)


def main():
    f = open("HeatMiserHeuristic.txt", "r")
    file = f.read()
    lines = file.split("\n")
    info = []
    for l in lines:
        info.append(l.split())
    info.pop(0)

    b = Building(info)
    count = 0
    while not b.isOpt():
        maxDifRoom = b.getMaxDifRoom()
        miserLocation = b.getRandomRoom()
        count += 1
        visited = []
        frontier = []
        heapq.heappush(frontier, (0, miserLocation))
        while frontier:
            oldMiser = miserLocation
            miserLocation = heapq.heappop(frontier)[1]
            if miserLocation == maxDifRoom:
                break
            visited.append(miserLocation)
            neighbors = b.getNeighbors(miserLocation)
            for n in neighbors:
                if n not in visited and n not in frontier:
                    heapq.heappush(frontier, (1.0 / b.getEdge(oldMiser, n), n))

        b.setRoomOpt(maxDifRoom)
    print(count)
    b.display()


if __name__ == "__main__":
    main()