import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

x = np.array([7, 9, 11, 13, 15, 17])
ylin = np.log10(np.array([980.709602394807, 1760.1525537105535, 3657.1918787042073, 6763.124291988286, 8538.121643747729, 14476.002348120015]))

x2 = np.array([7, 9, 11, 13, 15, 17])
# Use the original (non-log) y2 data
y2_orig = np.array([369.59979583002496,728.1208895558415,1530.893013277933,1602.8726737886486,1570.421493588681,1555.8021506796986])

# Log-transform for plotting with y2
y2 = np.log10(y2_orig)

# Fit exponential tapering: y = A * exp(-k * x) + C
def exp_taper(x, A, k, C):
    return A * np.exp(-k * x) + C

# Fit the exponential model to the original (non-log) y2 data
popt, _ = curve_fit(exp_taper, x2, y2, p0=(2000, 0.1, 1000))

# Generate fit line for plotting
x2_fit = np.linspace(min(x2), max(x2), 100)
y2_fit_orig = exp_taper(x2_fit, *popt)
# Log-transform the fit for plotting
y2_fit = y2_fit_orig

plt.plot(x2_fit, y2_fit, color='purple')

coeffs = np.polyfit(x, ylin, 1)
m, b = coeffs
x_linfit = np.linspace(min(x), max(x), 100)
y_linfit = m * x_linfit + b

plt.scatter(x, ylin, color='green', label='Optimal r_defect')
plt.plot(x_linfit, y_linfit, color='green')
plt.scatter(x2, y2, color='purple')  # Added line

plt.xlabel('System Size')
plt.ylabel('Log(Q)')
plt.title('Linear Fit to Data')
plt.legend()
plt.show()
plt.xlim(7, 17)
plt.ylim(2.5, 4.5)
plt.savefig("linear.pdf", format="pdf")
