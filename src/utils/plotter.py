# from itertools import count
import csv
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use("fivethirtyeight")

# index = count()

def _animate(i, fname="arduino_data.csv"):
    data = genfromtxt(fname, delimiter=",")
    if np.any(np.isnan(data[0])):
        with open(fname, "r") as f:
            reader = csv.reader(f)
            labels = next(reader)
        data = data[1:]    # remove fieldnames if any   
        data = data.T
    else:
        data = data.T
        labels=["column %d"%(i+1) for i in range(len(data))]

    plt.cla()

    for i in range(len(data)):
        plt.plot(data[i], label=labels[i])

    plt.legend(loc="upper left")
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), _animate, interval=500)

plt.tight_layout()
plt.show()

