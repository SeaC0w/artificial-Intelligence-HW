import plotly
import plotly.offline as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='connellyj', api_key='5qi8J7UttgRCvn0Vfkfm')


SAFE = 'Safe'
COMPLIANT = 'Compliant'
NON_COMPLIANT = 'NonCompliant'
NON_COMPLIANT2 = "Non-Compliant"
AGG = 'Aggregate'
OFFICE = 'Office'
WAREHOUSE = 'Warehouse'


def parse_input_test():
    f = open('HW3_Data.txt', 'r')
    file = f.read()
    lines = file.split('\n')
    lines.pop(0)
    d = {SAFE: 1, NON_COMPLIANT: 2, NON_COMPLIANT2: 2, COMPLIANT: 3}
    splitLines = [l.split() for l in lines]
    finalLines = [l[1:3] for l in splitLines]
    oshaLines = [d[l[-1]] for l in splitLines]
    for l in finalLines:
        for i, p in enumerate(l):
            l[i] = float(p)
    return finalLines, oshaLines


def parse_input_by_loc():
    f = open('HW3_Data.txt', 'r')
    file = f.read()
    lines = file.split('\n')
    lines.pop(0)
    splitLines = [l.split() for l in lines]
    finalLines = [l[1:4] for l in splitLines]
    for l in finalLines:
        for i, p in enumerate(l[:-1]):
            l[i] = float(p)
    return finalLines


def plot_by_osha():
    rawData, osha = parse_input_test()
    compliant = []
    noncompliant = []
    safe = []
    for i in range(len(osha)):
        if osha[i] == 1:
            safe.append((rawData[i][0], rawData[i][1]))
        elif osha[i] == 2:
            noncompliant.append((rawData[i][0], rawData[i][1]))
        else:
            compliant.append((rawData[i][0], rawData[i][1]))
    pointsSafe = go.Scatter(
        x=[l[0] for l in safe],
        y=[l[1] for l in safe],
        mode="markers",
        name="Safe"
    )
    pointsNon = go.Scatter(
        x=[l[0] for l in noncompliant],
        y=[l[1] for l in noncompliant],
        mode="markers",
        name="NonCompliant"
    )
    pointsComp = go.Scatter(
        x=[l[0] for l in compliant],
        y=[l[1] for l in compliant],
        mode="markers",
        name="Compliant"
    )
    data = [pointsSafe, pointsNon, pointsComp]
    fig = dict(data=data)
    py.plot(fig, filename='plot-by-osha.html')


def plot_by_location():
    rawData = parse_input_by_loc()
    office = []
    warehouse = []
    for i, d in enumerate(rawData):
        if d[2] == OFFICE:
            office.append((rawData[i][0], rawData[i][1]))
        elif d[2] == WAREHOUSE:
            warehouse.append((rawData[i][0], rawData[i][1]))
    officePoints = go.Scatter(
        x=[l[0] for l in office],
        y=[l[1] for l in office],
        mode="markers",
        name="Office"
    )
    warehousePoints = go.Scatter(
        x=[l[0] for l in warehouse],
        y=[l[1] for l in warehouse],
        mode="markers",
        name="Warehouse"
    )
    data = [officePoints, warehousePoints]
    fig = dict(data=data)
    py.plot(fig, filename='plot-by-loc.html')


def main():
    plot_by_osha()
    plot_by_location()


if __name__ == '__main__':
    main()
