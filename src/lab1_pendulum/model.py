from math import sin, sqrt

from src.general.constants import *
from .constants import *


def model(mode: Literal["basic", "windage"]) -> None:

	# constants for faster calculations
	k: Final[float] = g * dt ** 2 / l

	# setting start values of time and angle
	alpha_last = alpha_start
	alpha_cur = alpha_last
	t = 0.

	# initialization of datasets
	time_array = np.arange(0, t_max, dt)
	alpha_array = []

	n: Final[int] = len(time_array)

	datapath = datapath_basic if mode == "basic" else datapath_windage

	if mode == "windage":
		k_windage = k_windage_div_m * dt

	for frame in tqdm(range(n)):  # main loop
		if mode == "basic":  # see ../README.md
			alpha_next = 2 * alpha_cur - alpha_last - k*sin(alpha_cur)
		else:
			alpha_next = (4 * alpha_cur - alpha_last * (2 - k_windage) - k * sin(alpha_cur)) / (2 + k_windage)  # noqa (`k_windage` is always determined when needed)

		alpha_last = alpha_cur
		alpha_cur = alpha_next

		alpha_array.append(alpha_next)

	with open(datapath, 'w') as f:  # exporting data to file
		print(dt,           file=f, sep="\n")
		print(l,            file=f, sep="\n")
		print(t_max,        file=f, sep="\n")
		print(n,            file=f, sep="\n")
		print(*time_array,  file=f)
		print(*alpha_array, file=f)
