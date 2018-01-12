# HeatMiser implementation by Kerim Celik and Julia Connelly
import random
import numpy
from tabulate import tabulate

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
    bigTabl = []
    while not (avgTempGood and avgHumidGood and stdDevTempGood and stdDevHumidGood):
        tabl = [index + 1]
        if not (avgTempGood and stdDevTempGood):
            if stdDevTemp < optTempDev + 0.1:
                if avgTemp < optTemp:
                    temps[index] += 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Temperature Increase")
                elif avgTemp >= optTemp + 1:
                    temps[index] -= 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Temperature Decrease")
                else:
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("No Action")
            else:
                if temps[index] < optTemp:
                    temps[index] += 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Temperature Increase")
                elif temps[index] >= optTemp + 1:
                    temps[index] -= 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Temperature Decrease")
                else:
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("No Action")
            avgTemp = getListAverage(temps)
            stdDevTemp = getListStdDev(temps)
        else:
            if stdDevHumid < optHumidDev + 0.01:
                if avgHumid < optHumid:
                    humids[index] += 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Humidity Increase")
                elif avgHumid >= optHumid + 1:
                    humids[index] -= 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Humidity Increase")
                else:
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("No Action")
            else:
                if humids[index] < optHumid:
                    humids[index] += 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Humidity Increase")
                elif humids[index] >= optHumid + 1:
                    humids[index] -= 1
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("Humidity Increase")
                else:
                    tabl.append(temps[index])
                    tabl.append(humids[index])
                    tabl.append("No Action")
            avgHumid = getListAverage(humids)
            stdDevHumid = getListStdDev(humids)
        index += 1
        count += 1
        if (index == 12):
            index = 0
        avgTempGood = inRange(avgTemp, optTemp)
        avgHumidGood = inRange(avgHumid, optHumid)
        stdDevTempGood = stdDevTemp < optTempDev + 0.1
        stdDevHumidGood = stdDevHumid < optHumidDev + 0.01

        tabl.append(avgTemp)
        tabl.append(stdDevTemp)
        tabl.append(avgHumid)
        tabl.append(stdDevHumid)
        bigTabl.append(tabl)

    print(tabulate(bigTabl, headers=["Room #", "Temperature", "Humidity", "HeatMiser's Decision", "Average Temp", "Temp StdDev", "Average Humidity", "Humidity StdDev"], tablefmt="grid"))
    print("Total number of rooms visited by HeatMiser: " + str(count))
    print("\n")
    print("FINAL STATE OF ROOMS")
    print(tabulate([rooms, temps, humids], showindex=rowIDs, tablefmt="grid"))
    print("FINAL AVERAGE TEMPERATURE: " + str(avgTemp))
    print("FINAL TEMPERATURE STD DEV: " + str(stdDevTemp))
    print("FINAL AVERAGE HUMIDITY: " + str(avgHumid))
    print("FINAL HUMIDITY STD DEV: " + str(stdDevHumid))
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
