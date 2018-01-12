# HeatMiser implementation by Kerim Celik and Julia Connelly
import random
import numpy


def getListAverage(ls):
    return sum(ls) / len(ls)


def getListStdDev(ls):
    return numpy.std(ls)


def inRange(num, opt):
    return opt <= num < opt + 1


def main():
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

    # HeatMiser does the problem
    index = 0
    numberOfRounds = 0
    avgTemp = getListAverage(temps)
    avgHumid = getListAverage(humids)
    stdDevTemp = getListStdDev(temps)
    stdDevHumid = getListStdDev(humids)

    avgTempGood = inRange(avgTemp, optTemp)
    avgHumidGood = inRange(avgHumid, optHumid)
    stdDevTempGood = stdDevTemp < optTempDev + 0.1
    stdDevHumidGood = stdDevHumid < optHumidDev + 0.01

    print(temps)
    print(humids)
    print("\n")
    while not (avgTempGood and avgHumidGood and stdDevTempGood and stdDevHumidGood):
        if not (avgTempGood and stdDevTempGood):
            if stdDevTemp < optTempDev + 0.1:
                if avgTemp < optTemp:
                    temps[index] += 1
                elif avgTemp >= optTemp + 1:
                    temps[index] -= 1
            else:
                if temps[index] < optTemp:
                    temps[index] += 1
                elif temps[index] >= optTemp + 1:
                    temps[index] -= 1
        else:
            if stdDevHumid < optHumidDev + 0.01:
                if avgHumid < optHumid:
                    humids[index] += 1
                elif avgHumid >= optHumid + 1:
                    humids[index] -= 1
            else:
                if humids[index] < optHumid:
                    humids[index] += 1
                elif humids[index] >= optHumid + 1:
                    humids[index] -= 1
                else:
                    print("HeatMiser does nothing in room " + str(index) + ".")
        index += 1
        if index == 12:
            index = 0
        numberOfRounds += 1
        avgTemp = getListAverage(temps)
        avgHumid = getListAverage(humids)
        stdDevTemp = getListStdDev(temps)
        stdDevHumid = getListStdDev(humids)
        avgTempGood = inRange(avgTemp, optTemp)
        avgHumidGood = inRange(avgHumid, optHumid)
        stdDevTempGood = stdDevTemp < optTempDev + 0.1
        stdDevHumidGood = stdDevHumid < optHumidDev + 0.01
    print(temps)
    print(humids)
    print("\n")
    print(avgTemp)
    print(avgHumid)
    print(numberOfRounds)


if __name__ == "__main__":
    main()
