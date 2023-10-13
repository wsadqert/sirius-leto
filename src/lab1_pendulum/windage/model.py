from math import sin

from src.lab1_pendulum.windage.constants import *
from src.general.constants import *


# constants for faster calculations
k1 = k_windage_div_m * dt
k2 = 2 * g * dt ** 2 / l

# setting start values of time and angle
alpha_last = alpha_start
alpha_cur = alpha_last
t = 0.

# initialization of datasets
time_array = np.arange(0, t_max, dt)
alpha_array = []

# TODO: remove `n`
n: Final[int] = len(time_array)

for frame in tqdm(range(n)):  # main loop
	alpha_next = (4*alpha_cur - alpha_last*(2-k1) - k2*sin(alpha_cur))/(2+k1)

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
