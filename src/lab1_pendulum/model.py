from typing import Final
import numpy as np
from math import sin
from cmath import (sqrt as csqrt,  # noqa:typo
                   sin as csin,  # noqa:typo
                   cos as ccos,  # noqa:typo
                   exp as cexp)  # noqa:typo
from tqdm import tqdm
import logging

from src.general.calculations import find_extremums, sign
from src.lab1_pendulum.constants import CONFIG


def model(config: CONFIG) -> dict[str, int | list | np.ndarray]:
	"""
	Main function, calculate the model.

	:param config: Dictionary with data, obtained from user input. The dictionary's keys are variable names, and values are variables' values.
	:return: None.
	"""
	# Warning: pls ignore "Unresolved reference" errors, don't try to fix them, they are defined 5 lines below

	logging.debug("Extracting data from config")

	alpha_start = config['alpha_start']
	beta = config['beta']
	c1 = config['c1']
	c2 = config['c2']
	calculate_extremums = config['calculate_extremums']
	calculate_theoretical = config['calculate_theoretical']
	dt = config['dt']
	gamma = config['gamma']
	t_max = config['t_max']

	logging.info("Preparing model for calculating")

	# setting start values of time and angle
	alpha_last = alpha_start
	alpha_cur = alpha_start

	# datasets initialization
	time_array = np.arange(0, t_max, dt, dtype=np.float64)
	alpha_array = []

	n: Final[int] = len(time_array)

	match config["windage_method"]:
		case 'linear':
			get_alpha = lambda x: (2 * alpha_cur - alpha_last * (1 - c1) - c2 * sin(alpha_cur)) / (1 + c1)  # noqa:E731 using lambda
		case 'quadratic':
			get_alpha = lambda x: 2 * alpha_cur - alpha_last - 2 * (alpha_cur - alpha_last)**2 * config['k'] / config['m'] * sign(alpha_cur - alpha_last) - c2 * sin(alpha_cur)  # noqa:E731 using lambda
		case 'realistic':  # not implemented yet
			raise NotImplementedError
			get_alpha = ...
		case _:  # never executed, but necessary to avoid a "May be refenced before assignment" warning at line 67 (`alpha_next = get_alpha(t)`) inside main loop
			raise ValueError

	if calculate_theoretical:
		theoretical_alpha_array = []
		__phi_beta_positive = lambda t: (alpha_start / 2 * ((1 + gamma / csqrt(beta)) * cexp((-gamma + csqrt(beta)) * t) + (1 - gamma / csqrt(beta)) * cexp((-gamma - csqrt(beta)) * t))).real  # noqa:E731 using lambda
		__phi_beta_negative_zero = lambda t: (alpha_start * cexp(-gamma * t) * (ccos(csqrt(-beta) * t) + gamma / csqrt(-beta) * csin(csqrt(-beta) * t))).real  # noqa:E731 using lambda

		get_theoretical_alpha = __phi_beta_positive if beta > 0 else __phi_beta_negative_zero

	logging.info("Starting model calculation")
	for t in tqdm(time_array):  # main loop
		alpha_next = get_alpha(t)

		if calculate_theoretical:
			alpha_theoretical_next = get_theoretical_alpha(t)  # noqa - `get_theoretical_alpha(...)` is always defined
			theoretical_alpha_array.append(alpha_theoretical_next)  # noqa - `theoretical_alpha_array` is always defined

		alpha_last = alpha_cur
		alpha_cur = alpha_next

		alpha_array.append(alpha_next)

	logging.info("Finding extremums")

	if calculate_extremums:
		extremums_x = find_extremums(alpha_array)
		extremums_y = [alpha_array[i] for i in extremums_x]
		extremums_x = extremums_x * dt  # noqa - dont refactor this pls, np cannot process `*=` operator
	
	if calculate_theoretical and calculate_extremums:
		extremums_theory_x = np.array(find_extremums(theoretical_alpha_array))
		extremums_theory_y = [theoretical_alpha_array[i] for i in extremums_theory_x]
		extremums_theory_x = extremums_theory_x * dt  # noqa - dont refactor this pls, np cannot process `*=` operator

	dataset = {
		'n': n,
		'time_array': time_array,
		'alpha_array': alpha_array
	}
	if calculate_extremums:
		dataset['extremums_x'] = extremums_x
		dataset['extremums_y'] = extremums_y
	if calculate_theoretical and calculate_extremums:
		dataset['extremums_theory_x'] = extremums_theory_x
		dataset['extremums_theory_y'] = extremums_theory_y
	if calculate_theoretical:
		dataset['theoretical_alpha_array'] = theoretical_alpha_array

	return dataset
