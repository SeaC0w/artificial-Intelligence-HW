from sklearn import tree
from sklearn import cluster
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='connellyj', api_key='5qi8J7UttgRCvn0Vfkfm')


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
    return finalLines, [l[-1] for l in lines]


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


def get_cluster(clusterNum, labels_array):
    return np.where(labels_array == clusterNum)[0]


def get_list_average(ls):
    return sum(ls) / len(ls)


def k_means_clustering(k):
    rawData, osha = parse_input_clustering()
    km = cluster.KMeans(n_clusters=k).fit(rawData)
    clusters = []
    for i in range(k):
        c = get_cluster(i, km.labels_)
        data = [rawData[i] for i in c]
        clusters.append(
            go.Scatter(
                x=[p[0] for p in data],
                y=[p[1] for p in data],
                mode='markers',
                name='cluster ' + str(i)
            )
        )
    layout = dict(
        title='kmeans k = ' + str(k),
        xaxis=dict(title='distance'),
        yaxis=dict(title='speed')
    )
    fig = dict(data=clusters, layout=layout)
    py.plot(fig, filename='kmeans k = ' + str(k))


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
    py.plot(fig, filename='elbow-method')


def main():
    decision_tree()
    # NOTE!! Running any of the lines below will overwrite graphs stored online in plotly
    # elbow_method()
    # k_means_clustering(2)
    # k_means_clustering(3)
    # k_means_clustering(4)


if __name__ == '__main__':
    main()
