from sklearn import tree
import plotly
import plotly.offline as py
import plotly.graph_objs as go
import graphviz


plotly.tools.set_credentials_file(username='connellyj', api_key='5qi8J7UttgRCvn0Vfkfm')


SAFE = 'Safe'
COMPLIANT = 'Compliant'
NON_COMPLIANT = 'NonCompliant'
NON_COMPLIANT2 = "Non-Compliant"
AGG = 'Aggregate'
OFFICE = 'Office'
WAREHOUSE = 'Warehouse'
SPEED_CUT1 = 20
SPEED_CUT2 = 20
SPEED_CUT3 = 20
DIST_CUT = 100


def parse_input():
    stringMap = {OFFICE: 0, WAREHOUSE: 1}
    f = open('HW3_Data.txt', 'r')
    file = f.read()
    lines = file.split('\n')
    lines.pop(0)
    splitLines = [l.split() for l in lines]
    noIdLines = [l[1:-1] for l in splitLines]
    for l in noIdLines:
        l[2] = stringMap[l[2]]
        if float(l[1]) < SPEED_CUT1:
            l[1] = 1
        elif float(l[1]) < SPEED_CUT2:
            l[1] = 2
        elif float(l[1]) < SPEED_CUT3:
            l[1] = 3
        else:
            l[1] = 4
        if float(l[0]) < DIST_CUT:
            l[0] = 1
        else:
            l[0] = 2
    oshaLines = [l[-1] for l in splitLines]
    for i, w in enumerate(oshaLines):
        if w == NON_COMPLIANT2:
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


def calc_performance(pCount, rCount, eCount):
    recall = {}
    precision = {}
    f1s = {}
    for t in [SAFE, COMPLIANT, NON_COMPLIANT]:
        recall[t] = pCount[t] / rCount[t]
        if pCount[t] == 0:
            precision[t] = 1.0
        else:
            precision[t] = eCount[t] / pCount[t]
        f1s[t] = 2.0 * ((precision[t] * recall[t]) / (precision[t] + recall[t]))
    recall[AGG] = sum(list(recall.values())) / 3
    precision[AGG] = sum(list(precision.values())) / 3
    f1s[AGG] = sum(list(f1s.values())) / 3
    return recall, precision, f1s


def display_fold(recall, precision, f1s, foldNum, base):
    title = '' if not base else 'Baseline '
    print('*************** ' + title + 'Fold #' + str(foldNum) + ' ***************')
    print('Recall:')
    for k, v in recall.items():
        print('- ' + k + ': ' + str(v))
    print('Precision:')
    for k, v in precision.items():
        print('- ' + k + ': ' + str(v))
    print('F1-Score:')
    for k, v in f1s.items():
        print('- ' + k + ': ' + str(v))
    print('****************************************')
    print()


def display_overall(recallList, precisionList, f1List, base):
    recallTotal = {SAFE: 0, COMPLIANT: 0, NON_COMPLIANT: 0, AGG: 0}
    precisionTotal = {SAFE: 0, COMPLIANT: 0, NON_COMPLIANT: 0, AGG: 0}
    f1Total = {SAFE: 0, COMPLIANT: 0, NON_COMPLIANT: 0, AGG: 0}
    for label in [SAFE, COMPLIANT, NON_COMPLIANT, AGG]:
        for d in recallList:
            recallTotal[label] += d[label]
        for d in precisionList:
            precisionTotal[label] += d[label]
        for d in f1List:
            f1Total[label] += d[label]
    title = '' if not base else 'Baseline '
    start = 'Overall' if not base else 'Baseline Overall'
    print(title + 'Evaluation over All Folds:')
    print(start + ' Recall:')
    for k, v in recallTotal.items():
        print('- ' + k + ': ' + str(v / 10))
    print(start + ' Precision:')
    for k, v in precisionTotal.items():
        print('- ' + k + ': ' + str(v / 10))
    print(start + ' F1-Score:')
    for k, v in f1Total.items():
        print('- ' + k + ': ' + str(v / 10))
    print()


def plot_baseline(numFolds, recallList, precisionList, f1List, baseRecallList, basePrecisionList, baseF1List):
    recallLines = []
    precisionLines = []
    f1Lines = []
    recallLines.append(
        go.Scatter(
            x=[i for i in range(1, numFolds + 1)],
            y=[abs(1 - r[AGG]) for r in recallList],
            name='Recall'
        )
    )
    recallLines.append(
        go.Scatter(
            x=[i for i in range(1, numFolds + 1)],
            y=[abs(1 - r[AGG]) for r in baseRecallList],
            name='Baseline Recall'
        )
    )
    precisionLines.append(
        go.Scatter(
            x=[i for i in range(1, numFolds + 1)],
            y=[abs(1 - r[AGG]) for r in precisionList],
            name='Precision'
        )
    )
    precisionLines.append(
        go.Scatter(
            x=[i for i in range(1, numFolds + 1)],
            y=[abs(1 - r[AGG]) for r in basePrecisionList],
            name='Baseline Precision'
        )
    )
    f1Lines.append(
        go.Scatter(
            x=[i for i in range(1, numFolds + 1)],
            y=[r[AGG] for r in f1List],
            name='F1'
        )
    )
    f1Lines.append(
        go.Scatter(
            x=[i for i in range(1, numFolds + 1)],
            y=[r[AGG] for r in baseF1List],
            name='Baseline F1'
        )
    )
    fig = dict(
        data=recallLines,
        layout=dict(
            title='Baseline Recall All Classes',
            xaxis=dict(title='fold #', zeroline=True),
            yaxis=dict(title='distance from 1', range=[-0.1, 1.3])
        )
    )
    py.plot(fig, filename='recall-baseline.html')
    fig = dict(
        data=precisionLines,
        layout=dict(
            title='Baseline Precision All Classes',
            xaxis=dict(title='fold #', zeroline=True),
            yaxis=dict(title='distance from 1', range=[-0.1, 1.3])
        )
    )
    py.plot(fig, filename='precision-baseline.html')
    fig = dict(
        data=f1Lines,
        layout=dict(
            title='Baseline F1 All Classes',
            xaxis=dict(title='fold #', zeroline=True),
            yaxis=dict(title='F1', range=[-0.1, 1.3])
        )
    )
    py.plot(fig, filename='f1-baseline.html')


def decision_tree():
    data, osha = parse_input()
    splitData, splitOsha = split_data(data, osha)

    predictions = []
    for i in range(len(splitData)):
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit([d for s in splitData[1:] for d in s], [d for s in splitOsha[1:] for d in s])
        predictions.append(clf.predict(splitData[0]))
        splitData = rotate(splitData)
        splitOsha = rotate(splitOsha)
        data = tree.export_graphviz(
            clf,
            out_file=None,
            feature_names=['Distance', 'Speed', 'Location'],
            class_names=[COMPLIANT, NON_COMPLIANT, SAFE],
            filled=True, rounded=True, special_characters=True
        )
        graph = graphviz.Source(data)
        graph.render('decision-tree' + str(i))

    recallList = []
    precisionList = []
    f1List = []
    baseRecallList = []
    basePrecisionList = []
    baseF1List = []
    for i, (p, r) in enumerate(zip(predictions, splitOsha)):
        pCount = count_osha(p)
        rCount = count_osha(r)
        eCount = count_osha_equal(p, r)
        recall, precision, f1s = calc_performance(pCount, rCount, eCount)

        baseline = max(rCount, key=rCount.get)
        baseECount = count_osha_equal(baseline, r)
        basePCount = {}
        for t in [SAFE, COMPLIANT, NON_COMPLIANT]:
            if t == baseline:
                basePCount[t] = len(predictions)
            else:
                basePCount[t] = 0
        baseRecall, basePrecision, baseF1 = calc_performance(basePCount, rCount, baseECount)

        display_fold(recall, precision, f1s, i + 1, False)
        display_fold(baseRecall, basePrecision, baseF1, i + 1, True)

        recallList.append(recall)
        precisionList.append(precision)
        f1List.append(f1s)
        baseRecallList.append(baseRecall)
        basePrecisionList.append(basePrecision)
        baseF1List.append(baseF1)

    display_overall(recallList, precisionList, f1List, False)
    display_overall(baseRecallList, basePrecisionList, baseF1List, True)
    plot_baseline(len(predictions), recallList, precisionList, f1List, baseRecallList, basePrecisionList, baseF1List)


def main():
    decision_tree()


if __name__ == '__main__':
    main()
