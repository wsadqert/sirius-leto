import numpy as np
from tqdm import tqdm
from math import sin
from cmath import (sqrt as csqrt,  # noqa:typo
                   sin as csin,  # noqa:typo
                   cos as ccos,  # noqa:typo
                   exp as cexp)  # noqa:typo

from src.general.constants import *
from src.general.calculations import *
from .constants import *


def model(config: dict[str, ...]) -> None:
	"""
	Main function, calculating the model.

	:param config: Dictionary with data, obtained from user input. The dictionary's keys are variable names, and values are variables' values.
	:return: None.
	"""
	# Warning: pls ignore "Unresolved reference" errors, dont try to fix them, they are defined at line 22

	for i in config.keys():
		globals()[i] = config[i]

	# setting start values of time and angle
	alpha_last = alpha_start
	alpha_cur = alpha_start

	# initialization of datasets
	time_array = np.arange(0, t_max, dt)
	alpha_array = []

	n: Final[int] = len(time_array)

	match config["windage_method"]:
		case 'linear':
			get_alpha = lambda x: (2 * alpha_cur - alpha_last * (1 - c1) - c2 * sin(alpha_cur)) / (1 + c1)  # noqa:E731 using lambda
		case 'quadratic':
			get_alpha = lambda x: 2 * alpha_cur - alpha_last - 2 * c1 * (alpha_cur-alpha_last) - c2 * sin(alpha_cur)  # noqa:E731 using lambda
		case 'realistic':  # not implemented yet
			get_alpha = ...
		case _:  # never executed, but necessary to avoid a "May be refenced before assignment" warning at line 54 inside main loop
			raise ValueError

	if calculate_theoretical:
		theoretical_alpha_array = []
		__phi_beta_positive = lambda t: (alpha_start / 2 * ((1 + gamma / csqrt(beta)) * cexp((-gamma + csqrt(beta)) * t) + (1 - gamma / csqrt(beta)) * cexp((-gamma - csqrt(beta)) * t))).real  # noqa:E731 using lambda
		__phi_beta_negative_zero = lambda t: (alpha_start * cexp(-gamma * t) * (ccos(csqrt(-beta) * t) + gamma) / csqrt(-beta) * csin(csqrt(-beta) * t)).real  # noqa:E731 using lambda

		get_theoretical_alpha = __phi_beta_positive if beta > 0 else __phi_beta_negative_zero

	for t in tqdm(time_array):  # main loop
		alpha_next = get_alpha(t)

		if calculate_theoretical:
			alpha_theoretical_next = get_theoretical_alpha(t)  # noqa - `get_theoretical_alpha(...)` is always defined
			theoretical_alpha_array.append(alpha_theoretical_next)  # noqa - `theoretical_alpha_array` is always defined

		alpha_last = alpha_cur
		alpha_cur = alpha_next

		alpha_array.append(alpha_next)

	if calculate_extremums:
		extremums_x = find_extremums(alpha_array)
		extremums_y = [alpha_array[i] for i in extremums_x]
		extremums_x = extremums_x * dt  # noqa - dont refactor this pls, np cannot process `*=` operator

	if calculate_theoretical and calculate_extremums:
		extremums_theory_x = np.array(find_extremums(theoretical_alpha_array))
		extremums_theory_y = [theoretical_alpha_array[i] for i in extremums_theory_x]
		extremums_theory_x = extremums_theory_x * dt  # noqa - dont refactor this pls, np cannot process `*=` operator

	with open(datapath_model, 'w') as f:  # noqa - datapath is always defined
		print(n,                            file=f)  # exporting data to file
		print(*time_array,                  file=f)
		print(*alpha_array,                 file=f)
		if calculate_extremums:
			print(*extremums_x,             file=f)  # noqa - extremums_x is always defined
			print(*extremums_y,             file=f)  # noqa - extremums_y is always defined

		if calculate_theoretical:
			print(*theoretical_alpha_array, file=f)
			if calculate_extremums:
				print(*extremums_theory_x,  file=f)  # noqa - extremums_theory_x is always defined
				print(*extremums_theory_y,  file=f)  # noqa - extremums_theory_y is always defined
