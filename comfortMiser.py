# by Kerim Celik and Julia Connelly for AI, 02/02/2018
import random
import numpy
import queue
import heapq
from tabulate import tabulate
import sys

# helper class for displaying data
class Table:

    def __init__(self):
        self.bigTable = []
        self.tables = [[]]
        self.curTable = 0

    def nextTable(self):
        self.bigTable.append(self.tables[self.curTable])
        self.tables.append([])
        self.curTable += 1

    def addToTable(self, *arg):
        for i in arg:
            self.tables[self.curTable].append(i)

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


class StrategyBFS:
    def __init__(self):
        self.frontier = queue.Queue()

    def getFromFrontier(self):
        return self.frontier.get()

    def addToFrontier(self, prio, item):
        self.frontier.put((prio, item))

    def isEmpty(self):
        return self.frontier.empty()


class StrategyGreedyBestFirst:
    def __init__(self):
        self.frontier = []

    def getFromFrontier(self):
        return heapq.heappop(self.frontier)

    def addToFrontier(self, prio, item):
        heapq.heappush(self.frontier, (prio, item))

    def isEmpty(self):
        return not self.frontier


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
        self.tempStdDev = 1.5
        self.humidStdDev = 1.75

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

    # def display(self):
    #     tablef = Table()
    #     for index, room in enumerate(self.roomList):
    #         table.addToTable(index + 1, room.temp, room.humid)
    #         table.nextTable()
    #     print("FINAL STATE OF ROOMS")
    #     print(tabulate(tablef.bigTable, headers=["Room #", "Room Temp", "Room Humidity"], tablefmt="grid"))
    #     # print("roomList len = " + str(len(self.roomList)))
    #
    #     attrList = [self.getAvgTemp(), self.getStdDevTemp(), self.getAvgHumid(), self.getStdDevHumid(),]
    #     print(tabulate(attrList, header=["Final Avg Temp", "Final Std Dev Temp", "Final Avg Humid", "Final Std Dev Humid", "Total Rooms Visited", "Total Power Used"]))
    #     print("Final Avg Temp: " + str(self.getAvgTemp()))
    #     print("Final Std Dev Temp: " + str(self.getStdDevTemp()))
    #     print("Final Avg Humid: " + str(self.getAvgHumid()))
    #     print("Final Std Dev Humid: " + str(self.getStdDevHumid()))

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


def run():
    f = open("HeatMiserHeuristic.txt", "r")
    file = f.read()
    lines = file.split("\n")
    info = []
    for l in lines:
        info.append(l.split())
    info.pop(0)

    if !(len(sys.argv) == 2):
        print("Error: invalid number of command line arguments; expected 2.")
        return

    if sys.argv[1] == "bfs":
        strategy = StrategyBFS()
    elif sys.argv[1] == "greedy":
        strategy = StrategyGreedyBestFirst()
    else:
        print("not a valid strategy")
        return

    b = Building(info)
    # print out initial state of rooms for the run
    table = Table()
    for index, room in enumerate(b.roomList):
        table.addToTable(index + 1, room.temp, room.humid)
        table.nextTable()
    print("INITIAL STATE OF ROOMS")
    print(tabulate(table.bigTable, headers=["Room #", "Room Temp", "Room Humidity"], tablefmt="grid"))

    count = 0
    totalPower = 0
    totalVisit = 0
    miserLocation = b.getRandomRoom()
    while not b.isOpt():
        table2 = Table()
        maxDifRoom = b.getMaxDifRoom()
        count += 1
        table2.addToTable(count)
        table2.addToTable(miserLocation)
        visited = []
        frontier = []
        searchCost = 0
        searchCount = 0
        strategy.addToFrontier(1, miserLocation)
        while frontier:
            searchCount += 1
            oldMiser = miserLocation
            popped = strategy.getFromFrontier()
            miserLocation = popped[1]
            searchCost = 1 / popped[0]

            if miserLocation == maxDifRoom:
                break
            visited.append(miserLocation)
            neighbors = b.getNeighbors(miserLocation)
            for n in neighbors:
                if n not in visited and n not in frontier:
                    strategy.addToFrontier(1.0 / b.getEdge(oldMiser, n), n)
        table2.addToTable(miserLocation, searchCount - 1, searchCost - 1, b.getAvgTemp(), b.getStdDevTemp(), b.getAvgHumid(), b.getStdDevHumid())
        table2.nextTable()
        print(tabulate(table2.bigTable, headers=["Run #", "Start Room", "Final Room", "Rooms Visited", "Search Cost", "New Avg Temp", "New Temp Std Dev", "New Avg Humid", "New Humid Std Dev"], tablefmt="grid"))
        b.setRoomOpt(maxDifRoom)
        totalPower += searchCost - 1
        totalVisit += searchCount - 1
    tablef = Table()
    for index, room in enumerate(b.roomList):
        tablef.addToTable(index + 1, room.temp, room.humid)
        tablef.nextTable()
    print("FINAL STATE OF ROOMS")
    print(tabulate(tablef.bigTable, headers=["Room #", "Room Temp", "Room Humidity"], tablefmt="grid"))
    attrList = [b.getAvgTemp(), b.getStdDevTemp(), b.getAvgHumid(), b.getStdDevHumid(), totalVisit, totalPower]
    print(tabulate([attrList], headers=["Final Avg Temp", "Final Std Dev Temp", "Final Avg Humid", "Final Std Dev Humid", "Total Rooms Visited", "Total Power Used"]))

def main():
    run()
    return


if __name__ == "__main__":
    main()
