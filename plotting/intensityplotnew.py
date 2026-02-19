import os
import h5py
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

files = [
    "rscan-2-ez-001134.44.h5"
]

# def plot(fn):
#     fn = "/Users/maggieshi/Desktop/SachinUROP/Plots/" + fn
#     with h5py.File(fn, "r") as f:
#         ez = f["/ez"][()]   # shape ~ (Z, Y, X) = (400,400,400)

#     # pick central z and y
#     z0 = ez.shape[0] // 2   # center in z
#     y0 = ez.shape[1] // 2   # center in y
#     x0 = ez.shape[2] // 2   # center in x

#     # take a line cut along x
#     # line = (np.abs(ez[z0, y0, :]))   # shape (X,)
#     line = np.abs(ez[:, y0, x0])   # shape (X,)
#     # line = np.abs(ez[z0, :, x0])   # shape (X,)

#     # build coordinate axis centered at 0
#     N = line.shape[0]       # e.g. 400
#     print(N)
#     x = np.arange(N) - N//2 # goes from -200 to +199 if N=400

#     # clip to 400*(31-18)/31/200 = 
#     # 200 - 56 = 144
#     # 200 + 56 = 256
#     start = N * (31 - 18) // 31 // 2
#     end = N - start
#     x = x[start+5:end-5]
#     line = line[start+5:end-5]
#     line = np.log(line)

#     plt.plot(x, line)
#     plt.xlabel("Position (relative to center)")
#     plt.ylabel("Ez field")
#     plt.title(f"Line cut at z={z0}, y={y0}")
#     plt.axvline(0, color="k", ls="--", lw=0.8)
#     plt.grid(True)
#     plt.show()

from scipy.signal import find_peaks

def plot(fn, peak_distance=12, prominence=None, height=None, width=None):
    fn = os.path.join(DATA_DIR, fn)
    with h5py.File(fn, "r") as f:
        ez = f["/ez"][()]   # shape ~ (Z, Y, X)

    # pick central z and y
    z0 = ez.shape[0] // 2
    y0 = ez.shape[1] // 2
    x0 = ez.shape[2] // 2

    # take a line cut (choose axis by uncommenting the one you want)
    # line = np.abs(ez[z0, y0, :])
    line = np.abs(ez[:, y0, x0])
    # line = np.abs(ez[z0, :, x0])

    # coordinate axis centered at 0
    N = line.shape[0]
    print(N)
    x = np.arange(N) - N//2

    # clip region (keeping your ±5 margin)
    start = N * (31 - 18) // 31 // 2
    end = N - start
    x = x[start+5:end-5]
    line = line[start+5:end-5]

    # log amplitude with epsilon to avoid -inf
    eps = 1e-300
    line = np.log(np.maximum(line, eps))

    # masks for the two fitting regions: [start, -25] and [25, end]
    left_mask = x <= -25
    right_mask = x >= 25

    xL, yL = x[left_mask], line[left_mask]
    xR, yR = x[right_mask], line[right_mask]

    # --- SciPy peak finding on each side ---
    # You can tune: distance (samples), prominence, height, width
    pL, _ = find_peaks(yL, distance=peak_distance, prominence=prominence, height=height, width=width)
    pR, _ = find_peaks(yR, distance=peak_distance, prominence=prominence, height=height, width=width)

    # If peaks are too few, fall back to all points on that side
    fits = {}
    if pL.size >= 2:
        m1, b1 = np.polyfit(xL[pL], yL[pL], 1)
        fits['left'] = (m1, b1)
    elif xL.size >= 2:
        m1, b1 = np.polyfit(xL, yL, 1)
        fits['left'] = (m1, b1)

    if pR.size >= 2:
        m2, b2 = np.polyfit(xR[pR], yR[pR], 1)
        fits['right'] = (m2, b2)
    elif xR.size >= 2:
        m2, b2 = np.polyfit(xR, yR, 1)
        fits['right'] = (m2, b2)

    # --- plot ---
    plt.plot(x, line, label="data", color="blue")
    plt.xlabel("Position (relative to center)")
    plt.ylabel("Ez field (log scale)")
    plt.title(f"Line cut at z={z0}, y={y0}")
    # plt.axvline(0, color="k", ls="--", lw=0.8)
    plt.grid(False)

    # show peaks used
    if pL.size:
        plt.plot(xL[pL], yL[pL], 'ro', ms=6, label="left peaks")
    if pR.size:
        plt.plot(xR[pR], yR[pR], 'ro', ms=6, label="right peaks")

    # overlay fitted lines as dotted red
    if 'left' in fits:
        m1, b1 = fits['left']
        plt.plot(xL, m1 * xL + b1, 'r:', lw=1.6, label="left fit (peaks)")
    if 'right' in fits:
        m2, b2 = fits['right']
        plt.plot(xR, m2 * xR + b2, 'r:', lw=1.6, label="right fit (peaks)")

    # plt.legend(loc="best")
    plt.savefig("intensityplotnew.pdf", format="pdf")
    plt.show()


for file in files:
    plot(file)