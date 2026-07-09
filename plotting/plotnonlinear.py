import numpy as np
import matplotlib.pyplot as plt

n = np.array([7, 9, 11, 13, 15, 17])
Q_opt = np.array([980.709602394807, 1760.1525537105535, 3657.1918787042073, 6763.124291988286, 8538.121643747729, 14476.002348120015])

n2 = np.array([7, 9, 11, 13, 15, 17])
Q_det = np.array([369.59979583002496,728.1208895558415,1530.893013277933,1602.8726737886486,1570.421493588681,1555.8021506796986])

# Power-law fit: Q ~ n^a  =>  log(Q) = a*log(n) + b
log_n = np.log10(n)
log_Q_opt = np.log10(Q_opt)
log_n2 = np.log10(n2)
log_Q_det = np.log10(Q_det)

a, b = np.polyfit(log_n, log_Q_opt, 1)
print(f"Power-law exponent a = {a:.4f}, intercept b = {b:.4f}")

log_n_fit = np.linspace(min(log_n), max(log_n), 100)
log_Q_fit = a * log_n_fit + b

plt.scatter(log_n, log_Q_opt, color='green', label='Optimal r_defect')
plt.plot(log_n_fit, log_Q_fit, '--', color='green', label=f'Power-law fit: a={a:.2f}')
plt.scatter(log_n2, log_Q_det, color='purple', label='Detuned r_defect')

plt.xlabel('Log(n)')
plt.ylabel('Log(Q)')
plt.title('Power-law Fit to Data')
plt.legend()
plt.savefig("powerlaw.pdf", format="pdf")
plt.show()
