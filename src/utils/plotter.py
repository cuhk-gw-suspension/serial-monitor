# from itertools import count
import csv
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def array2d_animate(fig, arr, labels):
    """Display plots of data from a constantly updating array

    Parameters:
    -----------
    arr: 1d or 2d array
        data to display, grouped in columns
    labels: list-like
        list of labels.
    x_axis: bool, optional
        Default to False.
        If True, treat the 1st column as the common x_axis.
        If is set to True with arr being 1d array, overide to False.
    """
    artist = plt.plot(arr)
    plt.legend(artist, labels)

    def _animate(i):

        artist.set_ydata(arr)
        plt.legend(artist, labels)
        plt.tight_layout()

    FuncAnimation(fig, _animate, interval=500)

    plt.tight_layout()
    plt.show()


def csv_animate(fname="arduino_data.csv"):
    """Display plots of data from an updating csv.

    Parameter:
    ----------
    fname: str
            string of the path to the csv.

    """

    plt.style.use("fivethirtyeight")

    def _animate(i, fname=fname):
        data = genfromtxt(fname, delimiter=",")
        if np.any(np.isnan(data[0])):
            with open(fname, "r") as f:
                reader = csv.reader(f)
                labels = next(reader)
            data = data[1:]  # remove fieldnames if any
            data = data.T
        else:
            data = data.T
            labels = ["column %d" % (j + 1) for j in range(len(data))]

        plt.cla()

        for j in range(len(data)):
            plt.plot(data[j], label=labels[j])

        plt.legend(loc="upper left")
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), _animate, interval=500)

    plt.tight_layout()
    plt.show()
