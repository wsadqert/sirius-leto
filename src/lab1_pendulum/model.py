import sys
from scipy.signal import argrelextrema
from math import sin, sqrt

sys.path.append('src/lab1_pendulum')
from constants_lab1 import *

sys.path.append('../general')
from general.constants import *


k: Final[float] = g * dt ** 2 / l
period_teor: Final[float] = 2*pi*sqrt(l/g)

alpha_last = 1
alpha_cur = alpha_last
t = 0.

time_array = np.arange(0, t_max, dt)
alpha_array = []
alpha_teor = np.cos(2*pi*time_array/period_teor)*alpha_last

n: Final[int] = len(time_array)

for frame in tqdm(range(n)):
	alpha_next = 2 * alpha_cur - alpha_last - k*sin(alpha_cur)

	alpha_last = alpha_cur
	alpha_cur = alpha_next

	alpha_array.append(alpha_next)

print((argrelextrema(np.array(alpha_array), np.greater)[0]*dt)[0])

with open(datapath, 'w') as f:
	print(dt,           file=f, sep="\n")
	print(l,            file=f, sep="\n")
	print(t_max,        file=f, sep="\n")
	print(n,            file=f, sep="\n")
	print(*time_array,  file=f)
	print(*alpha_array, file=f)

"""
plt.xlabel('t, sec')
plt.ylabel('alpha, rad')
plt.grid(True, linestyle='--')

plt.plot(time_array, alpha_array, label='simulation')
plt.plot(time_array, alpha_teor, color='red', linewidth=0.7, linestyle='--', label='theoretical')
plt.legend(loc='upper right')
plt.show()
"""