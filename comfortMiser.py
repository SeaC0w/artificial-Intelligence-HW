import random
import numpy
import queue


def onesInList(ls):
    ret = []
    for i in range(len(ls)):
        if ls[i] == 1:
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

    def display(self):
        rooms = list(map(lambda r: "temp: " + str(r.temp) + " humid: " + str(r.humid), self.roomList))
        print("avg temp: " + str(self.getAvgTemp()))
        print("std dev temp: " + str(self.getStdDevTemp()))
        print("avg humid: " + str(self.getAvgHumid()))
        print("std dev humid: " + str(self.getStdDevHumid()))
        print("rooms: ")
        for r in rooms:
            print(r)

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

    def getNeighbors(self, roomIndex):
        return onesInList(self.edgeMatrix[roomIndex])

    def getRandomRoom(self):
        return random.randint(0, self.numRooms - 1)

    def getAvgTemp(self):
        temps = map(lambda r : r.temp, self.roomList)
        return getListAverage(list(temps))

    def getAvgHumid(self):
        humids = map(lambda r : r.humid, self.roomList)
        return getListAverage(list(humids))

    def getStdDevTemp(self):
        temps = map(lambda r: r.temp, self.roomList)
        return getListStdDev(list(temps))

    def getStdDevHumid(self):
        humids = map(lambda r: r.humid, self.roomList)
        return getListStdDev(list(humids))

    def getOptDifference(self, room):
        return self.roomList[room].getOptDifference(self.optTemp, self.optHumid)

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
        count += 1
        miserLocation = b.getRandomRoom()
        maxDifSeen = 0
        maxDifIndex = miserLocation

        visited = []
        frontier = queue.Queue()
        frontier.put(miserLocation)
        while not frontier.empty():
            miserLocation = frontier.get()
            dif = b.getOptDifference(miserLocation)
            if dif > maxDifSeen:
                maxDifSeen = dif
                maxDifIndex = miserLocation
            visited.append(miserLocation)
            neighbors = b.getNeighbors(miserLocation)
            for n in neighbors:
                if n not in visited:
                    frontier.put(n)

        b.setRoomOpt(maxDifIndex)

    print(count)
    print(b.display())


if __name__ == "__main__":
    main()