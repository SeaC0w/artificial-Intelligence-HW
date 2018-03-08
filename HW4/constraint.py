# blurb
ROOMS = ["w1", "w2", "w3", "w4",
         "o1", "o2", "o3", "o4",
         "o5", "o6"]
TEMP = 0
HUMID = 1
PASS = 2
UNASSIGN = -1
COLORS = {TEMP, HUMID, PASS}
COLOR_NAMES = ['temp', 'humid', 'pass']


class Room:
    def __init__(self, rList):
        self.adjacentRooms = rList

    def getAdjacentRooms(self):
        return self.adjacentRooms


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


def forwardChecking(rList):
    initialColors = [UNASSIGN for r in rList]
    frontier = [initialColors]
    visited = []
    count = 0
    valid = []

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
            valid.append(cur)

        usedColors = set([cur[i] for i in rList[nextUnassigned].getAdjacentRooms()])
        newColors = COLORS - usedColors
        for c in newColors:
            n = cur[:]
            n[nextUnassigned] = c
            if n not in visited and n not in frontier:
                frontier.append(n)
    print("number of steps: " + str(count))
    print("valid arrangements:")
    for v in valid:
        print(str([ROOMS[j] + ": " + COLOR_NAMES[c] for j, c in enumerate(v)]))


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
    valid = []
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
            valid.append(cur)

        for c in COLORS:
            n = cur[:]
            n[nextUnassigned] = c
            if n not in visited and n not in frontier:
                frontier.append(n)
    print("number of steps: " + str(count))
    print("valid arrangements:")
    for v in valid:
        print(str([ROOMS[j] + ": " + COLOR_NAMES[c] for j, c in enumerate(v)]))


def main():
    print("BRUTE FORCE:")
    bruteForce(makeConstraints())
    print()
    print("FORWARD CHECKING:")
    forwardChecking(makeConstraints())


if __name__ == "__main__":
    main()
