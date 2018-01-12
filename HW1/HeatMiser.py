# HeatMiser implementation by Kerim Celik and Julia Connelly
import random
import numpy
from tabulate import tabulate

def getListAverage(ls):
    return sum(ls) / len(ls)

def getListStdDev(ls):
    return numpy.std(ls)

def inRange(num, opt):
    return (num >= opt and num < opt + 1)

def main():
    # set up rooms
    optTemp = 72
    optHumid = 47
    optTempDev = 1.5
    optHumidDev = 1.75
    temps = []
    humids = []
    for i in range(0,12):
        temps.append(random.randint(65,75))
        humids.append(random.randint(55,65))

    # HeatMiser does the problem
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
    rooms = []
    for i in range(1,13):
        rooms.append("Room " + str(i))
    rowIDs = ["Room Number", "Temp", "Humidity"]
    print("INITIAL STATE OF ROOMS")
    print(tabulate([rooms, temps, humids], showindex=rowIDs, tablefmt="grid"))
    print("\n")
    while not (avgTempGood and avgHumidGood and stdDevTempGood and stdDevHumidGood):
        tabl = []
        if (not (avgTempGood and stdDevTempGood)):
            if (temps[index] < optTemp):
                print("HeatMiser raised the temperature in Room " + str(index) + " by 1 degree.")
                temps[index] += 1
                table = ["Visit " + str(count + 1), "Office " + str(index + 1), temps[index], humids[index], "Temperature Up"]
            elif (temps[index] >= optTemp + 1):
                print("HeatMiser lowered the temperature in Room " + str(index) + " by 1 degree.")
                temps[index] -= 1
#            else:
#                if (humids[index] < optHumid):
#                    #print("c")
#                    humids[index] += 1
#                elif (humids[index] >= optHumid + 1):
#                    #print("d")
#                    humids[index] -= 1
        else:
            if (humids[index] < optHumid):
                print("HeatMiser raised the humidity in Room " + str(index) + " by 1 percent.")
                humids[index] += 1
            elif (humids[index] >= optHumid + 1):
                print("HeatMiser lowered the humidity in Room " + str(index) + " by 1 percent.")
                humids[index] -= 1
            else:
                print("HeatMiser does nothing in room " + str(index) + ".")
        index += 1
        count += 1
        if (index == 12):
            index = 0
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



if __name__ == "__main__":
    main()
