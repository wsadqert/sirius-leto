from math import sin, sqrt

from src.lab1_pendulum.basic.constants import *
from src.general.constants import *


# constants for faster calculations
k: Final[float] = g * dt ** 2 / l
period_teor: Final[float] = 2*pi*sqrt(l/g)

# setting start values of time and angle
alpha_last = alpha_start
alpha_cur = alpha_last
t = 0.

# initialization of datasets
time_array = np.arange(0, t_max, dt)
alpha_array = []
alpha_teor = np.cos(2*pi*time_array/period_teor)*alpha_last

# TODO: remove `n`
n: Final[int] = len(time_array)

for frame in tqdm(range(n)):  # main loop
	alpha_next = 2 * alpha_cur - alpha_last - k*sin(alpha_cur)

	alpha_last = alpha_cur
	alpha_cur = alpha_next

	alpha_array.append(alpha_next)

# print((argrelextrema(np.array(alpha_array), np.greater)[0]*dt)[0])  # finding extremum

with open(datapath, 'w') as f:  # exporting data to file
	print(dt,           file=f, sep="\n")
	print(l,            file=f, sep="\n")
	print(t_max,        file=f, sep="\n")
	print(n,            file=f, sep="\n")
	print(*time_array,  file=f)
	print(*alpha_array, file=f)
