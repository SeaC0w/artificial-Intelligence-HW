# HeatMiser implementation by Kerim Celik and Julia Connelly
import random
import numpy
from tabulate import tabulate


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


def getListAverage(ls):
    return sum(ls) / len(ls)


def getListStdDev(ls):
    return numpy.std(ls)


def inRange(num, opt):
    return opt <= num < opt + 1


def run():
    # set up rooms
    optTemp = 72
    optHumid = 47
    optTempDev = 1.5
    optHumidDev = 1.75
    temps = []
    humids = []
    for i in range(0, 12):
        temps.append(random.randint(65, 75))
        humids.append(random.randint(45, 55))

    # initialize variables
    index = 0
    count = 0
    avgTemp = getListAverage(temps)
    avgHumid = getListAverage(humids)
    stdDevTemp = getListStdDev(temps)
    stdDevHumid = getListStdDev(humids)
    avgTempGood = inRange(avgTemp, optTemp)
    avgHumidGood = inRange(avgHumid, optHumid)
    stdDevTempGood = stdDevTemp < optTempDev + 0.1
    stdDevHumidGood = stdDevHumid < optHumidDev + 0.01

    # initialize information display
    rooms = []
    for i in range(1, 13):
        rooms.append("Room " + str(i))
    rowIDs = ["Room Number", "Temp", "Humidity"]
    print("INITIAL STATE OF ROOMS")
    print(tabulate([rooms, temps, humids], showindex=rowIDs, tablefmt="grid"))
    print("\n")
    table = Table()

    # HeatMiser does the problem
    while not (avgTempGood and avgHumidGood and stdDevTempGood and stdDevHumidGood):
        # display information
        table.addToTable(index + 1)
        actionDescription = ""

        # if the temperature measures are not correct, change this room
        if not (avgTempGood and stdDevTempGood):
            # if the std dev is in range, adjust room base on current avg
            if stdDevTempGood:
                if avgTemp < optTemp:
                    temps[index] += 1
                    actionDescription = "Temperature Increase"
                elif avgTemp >= optTemp + 1:
                    temps[index] -= 1
                    actionDescription = "Temperature Decrease"
            # otherwise move temperature closer to desired average
            else:
                if temps[index] < optTemp:
                    temps[index] += 1
                    actionDescription = "Temperature Increase"
                elif temps[index] >= optTemp + 1:
                    temps[index] -= 1
                    actionDescription = "Temperature Decrease"
            avgTemp = getListAverage(temps)
            stdDevTemp = getListStdDev(temps)
        # otherwise, change the humidity
        else:
            # if the std dev is in range, adjust room base on current avg
            if stdDevHumidGood:
                if avgHumid < optHumid:
                    humids[index] += 1
                    actionDescription = "Humidity Increase"
                elif avgHumid >= optHumid + 1:
                    humids[index] -= 1
                    actionDescription = "Humidity Decrease"
            # otherwise move humidity closer to desired average
            else:
                if humids[index] < optHumid:
                    humids[index] += 1
                    actionDescription = "Humidity Increase"
                elif humids[index] >= optHumid + 1:
                    humids[index] -= 1
                    actionDescription = "Humidity Decrease"
            avgHumid = getListAverage(humids)
            stdDevHumid = getListStdDev(humids)

        # recalculate and reset values
        count += 1
        index += 1
        if index == 12:
            index = 0
        avgTempGood = inRange(avgTemp, optTemp)
        avgHumidGood = inRange(avgHumid, optHumid)
        stdDevTempGood = stdDevTemp < optTempDev + 0.1
        stdDevHumidGood = stdDevHumid < optHumidDev + 0.01

        # display information
        if actionDescription == "":
            actionDescription = "No Action"
        table.addToTable(temps[index], humids[index], actionDescription)
        table.addToTable(avgTemp, stdDevTemp, avgHumid, stdDevHumid)
        table.nextTable()

    # print stuff
    print(tabulate(table.bigTable, headers=["Room #", "Temperature", "Humidity", "HeatMiser's Decision", "Average Temp", "Temp StdDev", "Average Humidity", "Humidity StdDev"], tablefmt="grid"))
    print("Total number of rooms visited by HeatMiser: " + str(count))
    print("\n")
    print("FINAL STATE OF ROOMS")
    print(tabulate([rooms, temps, humids], showindex=rowIDs, tablefmt="grid"))
    print("FINAL AVERAGE TEMPERATURE: " + str(avgTemp))
    print("FINAL TEMPERATURE STD DEV: " + str(stdDevTemp))
    print("FINAL AVERAGE HUMIDITY: " + str(avgHumid))
    print("FINAL HUMIDITY STD DEV: " + str(stdDevHumid))
    print("TOTAL NUMBER OF VISITS: " + str(count))
    print("\n")
    return count


def main():
    numVisits = []
    for i in range(1,101):
        print("Run " + str(i))
        numVisits.append(run())
    print("Average Number of Rooms Visited by HeatMiser over 100 Simulations: " + str(getListAverage(numVisits)))


if __name__ == "__main__":
    main()
