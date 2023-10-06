import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import g
from scipy.signal import argrelextrema
from math import sin
from tqdm import tqdm

l = 0.098
t_max = 5

alpha_last = 0.01
alpha_cur = 0.01
t = 0.

dt_array = np.array([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5, 7e-5, 8e-5, 9e-5, 1e-4, 2e-4, 3e-4, 4e-4, 5e-4, 6e-4, 7e-4, 8e-4, 9e-4, 1e-3, 2e-3, 3e-3, 4e-3, 5e-3, 6e-3, 7e-3, 8e-3, 9e-3, 1e-2, 2e-2, 3e-2, 4e-2, 5e-2, 6e-2, 7e-2, 8e-2, 9e-2, 1e-1])
period_array = []

for dt in tqdm(dt_array):
	n = int(t_max // dt)

	k = g * dt ** 2 / l
	alpha_array = [alpha_cur]
	for frame in range(n):
		alpha_next = 2 * alpha_cur - alpha_last - k*sin(alpha_cur)

		alpha_last = alpha_cur
		alpha_cur = alpha_next

		alpha_array.append(alpha_next)

	period_array.append((argrelextrema(np.array(alpha_array), np.greater)[0]*dt)[0 if dt == 1e-5 else 1])

plt.axhline(0.6281, linewidth=1, color='black', linestyle='--')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('dt, sec')
plt.ylabel('T, sec')
plt.grid(True, linestyle='--')

plt.plot(dt_array, period_array)
plt.show()
