import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import g
from scipy.signal import argrelextrema
from math import sin
from tqdm import tqdm
from rich.traceback import install

install(width=300, show_locals=True)

dt = 1e-5
l = 0.098
t_max = 100
k_windage_div_m = 1

n = int(t_max // dt)

k1 = k_windage_div_m * dt
k2 = 2 * g * dt ** 2 / l

alpha_last = 0.1
alpha_cur = alpha_last
t = 0.

time_array = np.arange(0, t_max, dt)
alpha_array = [alpha_cur]

for frame in tqdm(range(n)):
	alpha_next = (4*alpha_cur - alpha_last*(2-k1) - k2*sin(alpha_cur))/(2+k1)

	alpha_last = alpha_cur
	alpha_cur = alpha_next

	alpha_array.append(alpha_next)

extremums = argrelextrema(np.array(alpha_array), np.greater)[0]*dt
periods = []
for i in range(len(extremums)-1, 0, -1):
	periods.append(extremums[i]-extremums[i-1])
periods.reverse()

plt.figure()
plt.xlabel('t, sec')
plt.ylabel('alpha, rad')
plt.grid(True, linestyle='--')

plt.plot(time_array, alpha_array)

plt.figure()
plt.plot(range(len(periods)), periods)

plt.show()
