import math
import random
import numpy


numRooms = 12
minTemp = 65
maxTemp = 75
optTemp = 72
minHumid = 45
maxHumid = 55
optHumid = 47
tempStdDev = 1.75
humidStdDev = 1.5


def onesInList(ls):
    for i in range(len(ls)):
        if ls[i] == 1:
            ret.append(i)
    return ret


def getListAverage(ls):
    return sum(ls) / len(ls)


def getListStdDev(ls):
    return numpy.std(ls)


class Room:
    def __init__(self, temp, humid):
        self.temp = temp
        self.humid = humid
        
    def adjustTemp(value):
        self.temp += value
        
    def adjustHumid(value):
        self.humid += value

        
class Building:
    def __init__(self):
        self.roomList = []
        for i in range(numRooms):
            x = Room(random.randint(minTemp, maxTemp), random.randint(minHumid, maxHumid))
            self.roomList.append(x)
        self.edgeMatrix = []
        self.edgeMatrix.append([0,1,1,0,0,0,0,0,0,0,0,0])
        self.edgeMatrix.append([1,0,0,1,0,0,0,0,0,0,0,0])
        self.edgeMatrix.append([1,0,0,0,0,0,1,0,0,0,0,0])
        self.edgeMatrix.append([0,1,0,0,1,1,0,0,1,0,0,0])
        self.edgeMatrix.append([0,0,0,1,0,0,0,1,0,0,0,0])
        self.edgeMatrix.append([0,0,0,1,0,0,1,0,0,0,0,0])
        self.edgeMatrix.append([0,0,1,0,0,1,0,0,0,1,0,0])
        self.edgeMatrix.append([0,0,0,0,1,0,0,0,1,0,0,0])
        self.edgeMatrix.append([0,0,0,1,0,0,0,1,0,1,0,0])
        self.edgeMatrix.append([0,0,0,0,0,0,1,0,1,0,0,0])
        self.edgeMatrix.append([0,0,0,0,0,0,0,0,0,1,0,1])
        self.edgeMatrix.append([0,0,0,0,0,0,0,0,0,0,1,0])
        
    def getNeighbors(roomIndex):
        return onesInList(self.edgeMatrix[roomIndex])
    
    def setRoomTemp():
        

    
def main():    
    b = Building()
    miserLocation = random.randint(0,numRooms - 1)
    maxDifSeen = math.abs(optTemp - b.roomList[miserLocation].temp) +  \ 
                 math.abs(optHumid - b.roomList[miserLocation].humid)
    maxDifIndex = miserLocation
    
    visited = []
    frontier = Queue()
    frontier.put(miserLocation)
    while(frontier):
        miserLocation = frontier.get()
        dif = math.abs(optTemp - b.roomList[miserLocation].temp) +  \ 
              math.abs(optHumid - b.roomList[miserLocation].humid)
        if dif > maxDifSeen:
            maxDifSeen = dif
            maxDifIndex = miserLocation
        visited.append(miserLocation)
        neighbors = b.getNeighbors(miserLocation)
        for n in neighbors:
            frontier.put(n)
                

if __name__ == "__main__":
    main()