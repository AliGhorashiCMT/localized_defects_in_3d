import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the model function
def Q_model(R, Q_max, A, alpha):
    return Q_max / (1 + A * np.exp(-2 * alpha * R))

# Data points
x = np.array([5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])

y = np.array([980.709602394807, 1760.1525537105535, 2213.039918189905, 6763.124291988286,8538.121643747729, 14476.002348120015])
# x = np.log(x)
# y = np.array([2.64738989087624, 2.442493737660819, 2.866235057433789, 3.306256234532558, 
#               3.3166676545918206, 3.477930244134802, 3.3502981043768103, 
#               3.5240893185780418, 3.411034195018088])

# this one is new linear
# y = np.log10([236.25617580900800, 908.3799739015920, 4707.3020640897100, 3850.360369340840, 4767.43297285175, 3983.918240607790, 5999.580632065750, 12454.829577892300, 16644.6626287792, 32637.47567557030])
# print(y)
# use this one, new nonlinear
y = np.log10([244.70138276758544, 339.13135372955844, 1535.5314026679912, 1656.461650503958, 1869.3731060312302, 1105.9928910525048, 4761.0622299279075, 4059.1844131832736, 6329.807552231721, 4964.723983175013, 6050.243559524241])

xlin = [5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
# xlin = np.log(xlin)

ylin = [2.738290190460796, 3.087550493915694, 3.3328687909191985, 3.67828459586364, 3.3680272629185164, 4.095337789442018, 4.513716561214126, 4.100122383827675]
ylin = np.log10([236.25617580900800, 908.3799739015920, 4707.3020640897100, 3850.360369340840, 4767.43297285175, 3983.918240607790, 5999.580632065750, 12454.829577892300, 16644.6626287792, 32637.47567557030])

#  Perform linear fit (y = mx + b)
coeffs = np.polyfit(xlin, ylin, 1)  # Degree 1 for linear fit
m, b = coeffs  # Slope and intercept

# Generate y values based on the linear fit
x_linfit = np.linspace(min(xlin), max(xlin), 100)  # Generate 100 points between min and max of x
y_linfit = m * x_linfit + b  # y = mx + b

# Initial guesses for Q_max, A, alpha
initial_guess = [3.5, 1, 0.1]

# Fit the model to the data
params, covariance = curve_fit(Q_model, x, y, p0=initial_guess)

# Extract the optimized parameters
Q_max_fit, A_fit, alpha_fit = params

# Print the fitted parameters
print(f"Fitted Parameters:\nQ_max: {Q_max_fit}\nA: {A_fit}\nalpha: {alpha_fit}")
print(f"Slope (m): {m}")
print(f"Intercept (b): {b}")

# Generate points for the fitted curve
x_fit = np.linspace(min(x), max(x), 100)
y_fit = Q_model(x_fit, Q_max_fit, A_fit, alpha_fit)

# Plot the data and the fitted curve
plt.scatter(x, y, color='purple', label='Data')
plt.scatter(xlin, ylin, color='green')
plt.plot()
# Plot the line of best fit
plt.plot(x_fit, y_fit, linewidth=3, label='Fitted Model', color='purple')
plt.plot(x_linfit, y_linfit, color='green', linewidth=3, label=f'Best Fit Line (y = {m:.2f}x + {b:.2f})')

plt.xlabel('R (System Size)')
plt.ylabel('Q (Quality Factor)')
# plt.legend()
plt.title('Fitted Curve for Q(R)')
plt.savefig("nonlinear.pdf", format="pdf")
plt.show()

