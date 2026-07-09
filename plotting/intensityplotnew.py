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

# Toggle: True -> log|x| vs log|amp| (power-law fit), False -> x vs log|amp| (exponential fit)
LOGLOG = True


def plot(fn, peak_distance=12, prominence=None, height=None, width=None, loglog=LOGLOG):
    fn = os.path.join(DATA_DIR, fn)
    with h5py.File(fn, "r", locking=False) as f:
        dset = f["/ez"]              # shape ~ (Z, Y, X), not loaded yet
        z0 = dset.shape[0] // 2
        y0 = dset.shape[1] // 2
        x0 = dset.shape[2] // 2
        # take a line cut (choose axis by uncommenting the one you want)
        # line = np.abs(dset[z0, y0, :])
        line = np.abs(dset[:, y0, x0])
        # line = np.abs(dset[z0, :, x0])

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
    log_amp = np.log(np.maximum(line, eps))

    # masks for the two fitting regions: [start, -25] and [25, end]
    left_mask = x <= -25
    right_mask = x >= 25

    xL, yL = x[left_mask], log_amp[left_mask]
    xR, yR = x[right_mask], log_amp[right_mask]

    # for log-log we fit against log|x| instead of x
    if loglog:
        xL_fit = np.log(np.abs(xL))
        xR_fit = np.log(np.abs(xR))
    else:
        xL_fit, xR_fit = xL, xR

    # --- SciPy peak finding on each side (in log-amplitude) ---
    pL, _ = find_peaks(yL, distance=peak_distance, prominence=prominence, height=height, width=width)
    pR, _ = find_peaks(yR, distance=peak_distance, prominence=prominence, height=height, width=width)

    # fit slope: amp ~ exp(m*x)            if loglog=False  -> m is exponential decay rate (1/length)
    #            amp ~ |x|^m               if loglog=True   -> m is power-law exponent
    # For the "last 4 peaks" fit: left outer peaks = pL[:4] (most negative x = rightmost on log-log),
    # right outer peaks = pR[-4:] (largest x = rightmost on log-log)
    pL_outer = pL[:4] if pL.size >= 4 else pL
    pR_outer = pR[-4:] if pR.size >= 4 else pR

    fits = {}
    fits_outer = {}
    if pL.size >= 2:
        m1, b1 = np.polyfit(xL_fit[pL], yL[pL], 1); fits['left'] = (m1, b1)
    elif xL.size >= 2:
        m1, b1 = np.polyfit(xL_fit, yL, 1);          fits['left'] = (m1, b1)
    if pR.size >= 2:
        m2, b2 = np.polyfit(xR_fit[pR], yR[pR], 1); fits['right'] = (m2, b2)
    elif xR.size >= 2:
        m2, b2 = np.polyfit(xR_fit, yR, 1);          fits['right'] = (m2, b2)
    if pL_outer.size >= 2:
        m1o, b1o = np.polyfit(xL_fit[pL_outer], yL[pL_outer], 1); fits_outer['left'] = (m1o, b1o)
    if pR_outer.size >= 2:
        m2o, b2o = np.polyfit(xR_fit[pR_outer], yR[pR_outer], 1); fits_outer['right'] = (m2o, b2o)

    slope_label = "power-law exponent" if loglog else "exp decay rate (per unit x)"
    if 'left' in fits:
        print(f"left  {slope_label} (all peaks):    {fits['left'][0]:.4f}")
    if 'left' in fits_outer:
        print(f"left  {slope_label} (outer 4 peaks): {fits_outer['left'][0]:.4f}")
    if 'right' in fits:
        print(f"right {slope_label} (all peaks):    {fits['right'][0]:.4f}")
    if 'right' in fits_outer:
        print(f"right {slope_label} (outer 4 peaks): {fits_outer['right'][0]:.4f}")

    # --- plot ---
    # plot in real units (|amp|, and |x| for log-log) so matplotlib's axis scales do the log
    fig, ax = plt.subplots()
    ax.set_yscale('log')

    if loglog:
        ax.set_xscale('log')
        # split sides because x must be positive on a log axis
        ax.plot(np.abs(xL), np.exp(yL), color="blue", label="data (left)")
        ax.plot(xR,         np.exp(yR), color="blue", label="data (right)")
        if pL.size: ax.plot(np.abs(xL[pL]), np.exp(yL[pL]), 'ro', ms=6, label="left peaks")
        if pR.size: ax.plot(xR[pR],         np.exp(yR[pR]), 'ro', ms=6, label="right peaks")
        if 'left' in fits:
            m1, b1 = fits['left']
            ax.plot(np.abs(xL), np.exp(m1 * xL_fit + b1), 'r:', lw=1.6,
                    label=f"left fit (all): slope={m1:.3f}")
        if 'right' in fits:
            m2, b2 = fits['right']
            ax.plot(xR, np.exp(m2 * xR_fit + b2), 'r:', lw=1.6,
                    label=f"right fit (all): slope={m2:.3f}")
        if 'left' in fits_outer:
            m1o, b1o = fits_outer['left']
            ax.plot(np.abs(xL), np.exp(m1o * xL_fit + b1o), 'm--', lw=1.6,
                    label=f"left fit (outer 4): slope={m1o:.3f}")
        if 'right' in fits_outer:
            m2o, b2o = fits_outer['right']
            ax.plot(xR, np.exp(m2o * xR_fit + b2o), 'm--', lw=1.6,
                    label=f"right fit (outer 4): slope={m2o:.3f}")
        ax.set_xlabel("|Position| (relative to center)")
        out_pdf = "intensityplotnew_loglog.pdf"
    else:
        ax.plot(x, np.exp(log_amp), color="blue", label="data")
        if pL.size: ax.plot(xL[pL], np.exp(yL[pL]), 'ro', ms=6, label="left peaks")
        if pR.size: ax.plot(xR[pR], np.exp(yR[pR]), 'ro', ms=6, label="right peaks")
        if 'left' in fits:
            m1, b1 = fits['left']
            ax.plot(xL, np.exp(m1 * xL + b1), 'r:', lw=1.6,
                    label=f"left fit (all): slope={m1:.4f}")
        if 'right' in fits:
            m2, b2 = fits['right']
            ax.plot(xR, np.exp(m2 * xR + b2), 'r:', lw=1.6,
                    label=f"right fit (all): slope={m2:.4f}")
        if 'left' in fits_outer:
            m1o, b1o = fits_outer['left']
            ax.plot(xL, np.exp(m1o * xL + b1o), 'm--', lw=1.6,
                    label=f"left fit (outer 4): slope={m1o:.4f}")
        if 'right' in fits_outer:
            m2o, b2o = fits_outer['right']
            ax.plot(xR, np.exp(m2o * xR + b2o), 'm--', lw=1.6,
                    label=f"right fit (outer 4): slope={m2o:.4f}")
        ax.set_xlabel("Position (relative to center)")
        out_pdf = "intensityplotnew.pdf"

    ax.set_ylabel("|Ez| field")
    ax.set_title(f"Line cut at z={z0}, y={y0}  ({'log-log' if loglog else 'semi-log'})")
    ax.grid(False)
    ax.legend(loc="best", fontsize=8)
    fig.savefig(out_pdf, format="pdf")
    plt.show()


for file in files:
    plot(file)