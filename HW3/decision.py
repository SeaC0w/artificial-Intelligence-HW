from sklearn import tree


SAFE = 'Safe'
COMPLIANT = 'Compliant'
NON_COMPLIANT = 'NonCompliant'


def parse_input():
    stringMap = {'Office': 0, 'Warehouse': 1}
    f = open('HW3_Data.txt', 'r')
    file = f.read()
    lines = file.split('\n')
    lines.pop(0)
    splitLines = [l.split() for l in lines]
    noIdLines = [l[1:-1] for l in splitLines]
    for l in noIdLines:
        l[2] = stringMap[l[2]]
    oshaLines = [l[-1] for l in splitLines]
    for i, w in enumerate(oshaLines):
        if w == 'Non-Compliant':
            oshaLines[i] = NON_COMPLIANT
    return noIdLines, oshaLines


def split_data(data, osha):
    splitData = []
    splitOsha = []
    for i in range(0, len(data), int(len(data) * 0.1)):
        splitData.append(data[i:i + int(len(data) * 0.1)])
        splitOsha.append(osha[i:i + int(len(data) * 0.1)])
    return splitData, splitOsha


def rotate(arr):
    popped = arr.pop(0)
    arr.append(popped)
    return arr


def count_osha(arr):
    counts = {SAFE: 0, COMPLIANT: 0, NON_COMPLIANT: 0}
    for i in arr:
        counts[i] += 1
    return counts


def count_osha_equal(arr1, arr2):
    eCount = {SAFE: 0, COMPLIANT: 0, NON_COMPLIANT: 0}
    for pi, ri in zip(arr1, arr2):
        if pi == ri:
            eCount[pi] += 1
    return eCount


def main():
    data, osha = parse_input()
    splitData, splitOsha = split_data(data, osha)

    predictions = []
    for i in range(len(splitData)):
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit([d for s in splitData[1:] for d in s], [d for s in splitOsha[1:] for d in s])
        predictions.append(clf.predict(splitData[0]))
        splitData = rotate(splitData)
        splitOsha = rotate(splitOsha)

    for i, (p, r) in enumerate(zip(predictions, splitOsha)):
        pCount = count_osha(p)
        rCount = count_osha(r)
        eCount = count_osha_equal(p, r)
        recall = {}
        precision = {}
        for t in [SAFE, COMPLIANT, NON_COMPLIANT]:
            recall[t] = pCount[t] / rCount[t]
            precision[t] = eCount[t] / pCount[t]

        print('Fold #' + str(i + 1))
        print('Recall:')
        for k, v in recall.items():
            print('- ' + k + ': ' + str(v))
        print('Precision:')
        for k, v in precision.items():
            print('- ' + k + ': ' + str(v))
        print()


if __name__ == '__main__':
    main()
