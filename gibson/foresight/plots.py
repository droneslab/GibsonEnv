import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

base_dir='/ubcse/drones/projects/foresight/results/gcp'
plot_dirs=['Vanilla', 'SSD', 'RAM']

for d in plot_dirs:
    pfile = '{}/{}/log/plot.csv'.format(base_dir, d)
    data = genfromtxt(pfile, delimiter=',')
    plt.plot(data[:,0], data[:,1], label=d)

plt.ylabel('Mean Episode Reward')
plt.xlabel('Time (seconds)')
plt.legend()
plt.show()
