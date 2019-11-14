import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

import csv

BASE_DIR='/ubcse/drones/projects/foresight/results/gcp'
PLOT_DIRS=['Vanilla', 'SSD']
PLOT_LABELS = ['value_loss','approxkl','policy_entropy','policy_loss','eprewmean','eplenmean'];

def parse(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        d = {name: [] for name in reader.fieldnames}
        for row in reader:
            for name in reader.fieldnames:
                try:
                    d[name].append(float(row[name]))
                except ValueError:
                    d[name].append(0)
    return d


def subplots(data, plotLabels):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 4))

    currentIndex=0
    for i in range(0,2):
        for ax in axes[i]:
            ax.set_title(plotLabels[currentIndex])
            for file in sorted(data.keys()):
                currData = data[file]
                currField = currData[plotLabels[currentIndex]]
                xAxis = currData["time_elapsed"]
                print(xAxis)
                ax.plot(xAxis, currField,label =file)
            currentIndex +=1
            ax.legend(loc="upper right")

    fig.tight_layout()
    plt.show()


def main(base_dir, plot_dirs, plotLabels):
    data = dict()
    for d in plot_dirs:
        pfile = '{}/{}/log/progress.csv'.format(base_dir, d)
        data[d] = parse(pfile)

    subplots(data, plotLabels)


if __name__ == "__main__":
    main(BASE_DIR, PLOT_DIRS, PLOT_LABELS)
