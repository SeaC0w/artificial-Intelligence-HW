import plotly
from sklearn import cluster
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='connellyj', api_key='5qi8J7UttgRCvn0Vfkfm')


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
    py.plot(fig, filename='k' + str(k) + '.html')


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
    elbow_method()
    for i in range(2, 5):
        k_means_clustering(i)


if __name__ == '__main__':
    main()
