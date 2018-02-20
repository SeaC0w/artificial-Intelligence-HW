import plotly
from sklearn import cluster
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='connellyj', api_key='5qi8J7UttgRCvn0Vfkfm')

SAFE = "Safe"
COMP = "Compliant"
NON_COMP = "NonCompliant"
AGG = "Aggregate"

def parse_input_clustering():
    f = open('HW3_Data.txt', 'r')
    file = f.read()
    lines = file.split('\n')
    lines.pop(0)
    splitLines = [l.split() for l in lines]
    finalLines = [l[1:3] for l in splitLines]
    for l in finalLines:
        for i, p in enumerate(l):
            l[i] = float(p)
    return finalLines, [l[-1] for l in splitLines]

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


def calc_performance(truePos, retrieve, relevant):
    recall = {}
    precision = {}
    f1s = {}
    for t in [SAFE, COMP, NON_COMP]:
        recall[t] = truePos[t] / relevant[t]
        # print("RECALL NON " + str(recall[NON_COMP]))
        if retrieve[t] == 0:
            precision[t] = 1.0
        else:
            precision[t] = truePos[t] / retrieve[t]
        # print("PRECISION NON " + str(precision[NON_COMP]))
        if truePos[t] == 0:
            f1s[t] = 0.0
        else:
            f1s[t] = 2.0 * ((precision[t] * recall[t]) / (precision[t] + recall[t]))
    recall[AGG] = sum(list(recall.values())) / 3
    precision[AGG] = sum(list(precision.values())) / 3
    f1s[AGG] = sum(list(f1s.values())) / 3
    return recall, precision, f1s


def display_fold(recall, precision, f1s, foldNum):
    title = ''
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


def display_overall(recallList, precisionList, f1List):
    recallTotal = {SAFE: 0, COMP: 0, NON_COMP: 0, AGG: 0}
    precisionTotal = {SAFE: 0, COMP: 0, NON_COMP: 0, AGG: 0}
    f1Total = {SAFE: 0, COMP: 0, NON_COMP: 0, AGG: 0}
    for label in [SAFE, COMP, NON_COMP, AGG]:
        for d in recallList:
            recallTotal[label] += d[label]
        for d in precisionList:
            precisionTotal[label] += d[label]
        for d in f1List:
            f1Total[label] += d[label]
    title = ''
    start = 'Overall'
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

def get_cluster(clusterNum, labels_array):
    return np.where(labels_array == clusterNum)[0]


def get_list_average(ls):
    return sum(ls) / len(ls)

def get_cluster_class(oshaList):
    amtSafe = 0
    amtComp = 0
    amtNonC = 0
    for s in oshaList:
        if s == SAFE:
            amtSafe += 1
        elif s == COMP:
            amtComp += 1
        else:
            amtNonC += 1
    if (amtSafe >= amtComp) and (amtSafe >= amtNonC):
        return SAFE
    elif (amtComp >= amtNonC):
        return COMP
    else:
        return NON_COMP


def k_means_clustering(k):
    rawData, osha = parse_input_clustering()
    for i in range(len(osha)):
        if osha[i] == "Non-Compliant":
            osha[i] = NON_COMP
    splitData, splitOsha = split_data(rawData, osha)
    recallList = []
    precisionList = []
    f1List = []
    for j in range(len(splitData)):
        joinData = [d for s in splitData[1:] for d in s]
        joinOsha = [d for s in splitOsha[1:] for d in s]
        testData = splitData[0]
        testOsha = splitOsha[0]
        splitData = rotate(splitData)
        splitOsha = rotate(splitOsha)
        km = cluster.KMeans(n_clusters=k).fit(joinData)
        clusters = []
        clusterClasses = []
        for i in range(k):
            # gets the cluster with the same label as i
            c = get_cluster(i, km.labels_)
            data = [joinData[x] for x in c]
            oshaTags = [joinOsha[x] for x in c]
            tag = get_cluster_class(oshaTags)
            clusterClasses.append(tag)
            clusters.append(
                go.Scatter(
                    x=[p[0] for p in data],
                    y=[p[1] for p in data],
                    mode='markers',
                    name=tag + ' ' + str(i)
                )
            )
        layout = dict(
            title='kmeans k = ' + str(k),
            xaxis=dict(title='distance'),
            yaxis=dict(title='speed')
        )
        fig = dict(data=clusters, layout=layout)
        py.plot(fig, filename='k' + str(k) + '.' + str(j) + '.html')

        truePos = {SAFE: 0, COMP: 0, NON_COMP: 0}
        retrieve = {SAFE: 0, COMP: 0, NON_COMP: 0}
        relevant = {SAFE: 0, COMP: 0, NON_COMP: 0}
        predictData = km.predict(testData)
        testPredicts = [clusterClasses[k] for k in predictData]
        for i in range(len(testPredicts)):
            guess = testPredicts[i]
            fact = testOsha[i]
            if guess == fact:
                truePos[guess] += 1
            retrieve[guess] += 1
            relevant[fact] += 1
        recall, precision, f1s = calc_performance(truePos, retrieve, relevant)
        display_fold(recall, precision, f1s, j + 1)
        recallList.append(recall)
        precisionList.append(precision)
        f1List.append(f1s)
    display_overall(recallList, precisionList, f1List)

def elbow_method():
    rawData, osha = parse_input_clustering()
    maxDist = max([p[0] for p in rawData])
    maxSpeed = max([p[1] for p in rawData])
    sse = {}
    for k in range(1, 10):
        sse[k] = 0
        kmeans = cluster.KMeans(n_clusters=k).fit(rawData)
        for i in range(k):
            c = get_cluster(i, kmeans.labels_)
            # normalize the data points (by dividing by max value)
            data = [[rawData[i][0] / maxDist for i in c], [rawData[i][1] / maxSpeed for i in c]]
            mean = [get_list_average(data[0]), get_list_average(data[1])]
            for j in range(len(data[0])):
                sse[k] += pow((float(data[0][j]) - mean[0]) + (float(data[1][j]) - mean[1]), 2)
    line = go.Scatter(
        x=list(sse.keys()),
        y=list(sse.values())
    )
    data = [line]
    layout = dict(
        title='Elbow Method',
        xaxis=dict(title='k'),
        yaxis=dict(title='sse')
    )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='elbow-method.html')


def main():
    # elbow_method()
    # for i in range(2,5):
    #     k_means_clustering(i)
    k_means_clustering(4)


if __name__ == '__main__':
    main()
