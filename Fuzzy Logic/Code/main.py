from scipy.spatial.distance import cdist
import pylab as plt
import pandas as pd
import numpy as np
import sys

EPSILON = 1e-5
MIN_CLUSTERS = 2
MAX_CLUSTERS = 8
m = 2

def main():
    sampleNumber = sys.argv[1]
    clusterCount = 4
    data = pd.read_csv("sample" + sampleNumber + ".csv").values
    centers, U = make_clusters(data, clusterCount)
    show_results(data, centers, U)


def normalize_over_axis(input, axis, denom=None):
    if denom is None:
        denom = input
    return (input.T/denom.sum(axis=axis)).T


def next_centers(data, U):
    u_m =  U ** m
    return normalize_over_axis(u_m.T @ data, 0, u_m)


def next_U(data, centers, sampleCount):
    exponent = 2 / (m - 1)
    fraction = cdist(data, centers) ** exponent
    denominator = fraction.reshape((sampleCount, 1, -1))
    denominator = denominator.repeat(fraction.shape[-1], axis=1)
    denominator = fraction[:, :, np.newaxis] / denominator
    return 1 / denominator.sum(2)


def make_clusters(data, clusterCount):
    sampleCount = data.shape[0]
    U = np.random.rand(sampleCount, clusterCount)
    U = normalize_over_axis(U, 1)
    error = 1
    while error > EPSILON:
        centers = next_centers(data, U)
        previous_U = U.copy()
        U = next_U(data, centers, sampleCount)
        #nansum to avoid having nans for big m s
        error = np.nansum(np.abs(U - previous_U))
    return centers, U


def show_results(data, centers, U):
    colorStore = ["or", "og", "oc", "om", "oy", "ok", "dodgerblue", "fuchsia"]
    plt.subplots(1, 1)
    for i, datum in enumerate(data):
        max_index = np.argmax(U[i])
        plt.plot(datum[0], datum[1], colorStore[max_index], zorder=1)
    # plt.scatter(data[:,0], data[:,1])
    plt.scatter(centers[:,0], centers[:,1], c='k', zorder=2)
    plt.show()


if __name__ == '__main__':
    main()