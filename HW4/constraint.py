# blurb
ROOMS = ["w1", "w2", "w3", "w4",
         "o1", "o2", "o3", "o4",
         "o5", "o6"]
TEMP = 0
HUMID = 1
PASS = 2
UNASSIGN = -1
COLORS = {TEMP, HUMID, PASS}


class Room:
    def __init__(self, rList):
        self.adjacentRooms = rList
        self.value = UNASSIGN

    def setAdjacentRooms(self, rList):
        self.adjacentRooms = rList

    def getAdjacentRooms(self):
        return self.adjacentRooms

    def setValue(self, v):
        self.value = v

    def getValue(self):
        return self.value


def makeConstraints():
    rList = [
        Room([1, 4, 5, 7, 8]),
        Room([0, 2, 5, 6]),
        Room([1, 3, 6]),
        Room([2, 7, 8, 9]),
        Room([0, 9]),
        Room([0, 1, 6, 7]),
        Room([1, 2, 5, 7]),
        Room([0, 3, 5, 6, 8]),
        Room([0, 3, 7, 9]),
        Room([3, 4, 8])]
    return rList


# returns string ID for location of room with the most constraints on it
def getMostConstrainedValue(roomList):
    return max(roomList, key=lambda r: len(r.getAdjacentRooms()))
    # amt = 0
    # track = 0
    # l = [len(roomList[i].getAdjacentRooms()) for i in roomList]
    # for j in l:
    #     if l[j] > amt:
    #         track = j
    #         amt = l[j]
    # return roomList[track]


def forwardChecking(rList):
    initialColors = [UNASSIGN for r in rList]
    frontier = [initialColors]
    visited = []
    count = 0
    while len(frontier) != 0:
        count += 1
        cur = frontier.pop(0)
        visited.append(cur)

        nextUnassigned = -1
        for i, c in enumerate(cur):
            if c == UNASSIGN:
                nextUnassigned = i
                break
        if nextUnassigned == -1:
            print(str(cur))

        usedColors = set([cur[i] for i in rList[nextUnassigned].getAdjacentRooms()])
        newColors = COLORS - usedColors
        for c in newColors:
            n = cur[:]
            n[nextUnassigned] = c
            if n not in visited and n not in frontier:
                frontier.append(n)
    print(str(count))


def isValid(colors, rList):
    for i, r in enumerate(rList):
        for n in r.getAdjacentRooms():
            if colors[i] == colors[n] and colors[n] != UNASSIGN and colors[i] != UNASSIGN:
                return False
    return True


def bruteForce(rList):
    initialColors = [UNASSIGN for r in rList]
    frontier = [initialColors]
    visited = []
    count = 0
    while len(frontier) != 0:
        count += 1
        cur = frontier.pop(0)
        visited.append(cur)

        if not isValid(cur, rList):
            continue

        nextUnassigned = -1
        for i, c in enumerate(cur):
            if c == UNASSIGN:
                nextUnassigned = i
                break
        if nextUnassigned == -1:
            print(str(cur))

        for c in COLORS:
            n = cur[:]
            n[nextUnassigned] = c
            if n not in visited and n not in frontier:
                frontier.append(n)
    print(str(count))


def main():
    bruteForce(makeConstraints())
    print()
    forwardChecking(makeConstraints())


if __name__ == "__main__":
    main()
