import csv
import peakutils
from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout, Figure


def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.read().split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].replace(";", ",")

        stream = csv.reader(lines, delimiter=',', quotechar='|')

        arr = []
        for row in stream:
            arr.append(row)
        return arr
# Get data of the specific chemical elements, which could be observed by a detector
def get_data_file1(file):
    file = read_file("D:/SIMS/file1.csv")
    file.pop(0)
    file.pop(0)
# ---------------------------------------------

    mass = []
    sem = []
    for i in file:
        if len(i) == 5:
            mass.append(float(i[3]))
            sem.append(float(i[4]))
    return mass, sem

# Get data of the all chemical elements, which have been measured by a detector
def get_data_file2(file):
    file.pop(0)
    dataDic = {}    
    for i in file:
        if len(i) > 0:
            key = int(i[0])
            dataDic[key] = []
            for j in i[1:len(i)]:
                if len(j) > 1:
                    dataDic[key].append(j)
    return dataDic


def get_peaks(mass, sem, thres):
    indexes = peakutils.indexes(sem, thres, min_dist)
    maxY = [sem[i] for i in indexes]
    maxX = [mass[i] for i in indexes]
    return maxX, maxY

# threshold of measured elements --------------
file1 = read_file("D:/SIMS/file1.csv")
file2 = read_file("D:/SIMS/file2.csv")
# ---------------------------------------------

mass, sem = get_data_file1(file1)
dataDic = get_data_file2(file2)

# threshold of measured elements --------------
thres = 1000 / max(sem)
min_dist = 1
# ---------------------------------------------

maxX, maxY = get_peaks(mass, sem, thres)
labels = []

for i in maxX:
    if int(i) in dataDic.keys():
        labels.append(",".join(dataDic[int(i)]))
    else:
        labels.append("#")

scat1 = Scatter(x=mass, y=sem, name ="Measured Spectrum", mode='lines+markers')
scat2 = Scatter(x=maxX, y=maxY, name="Identified Peak", mode='markers', 
                marker=dict(color='red',symbol="star", size=12), text=labels)

data = [scat1, scat2]
layout = Layout(xaxis=dict(title="Mass of elements, [amu]",visible=True, 
                rangeslider=dict(visible=True, range=[min(maxX), max(maxX)])),
                yaxis=dict(title="Counts per second",
                        type='log',autorange=True
                        ),
                           title="Identification of chemical elements"
)
figur = Figure(data=data, layout=layout)
plot(figur)




