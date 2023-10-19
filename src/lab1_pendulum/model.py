from math import sin
from cmath import (sqrt as csqrt,  # noqa:typo
                   sin as csin,  # noqa:typo
                   cos as ccos,  # noqa:typo
                   exp as cexp)  # noqa:typo

from src.general.constants import *
from .constants import *


def model() -> None:
	# setting start values of time and angle
	alpha_last = alpha_start
	alpha_cur = alpha_last

	# initialization of datasets
	time_array = np.arange(0, t_max, dt)
	alpha_array = []
	theoretical_alpha_array = []

	n: Final[int] = len(time_array)

	get_alpha = lambda x: (2 * alpha_cur - alpha_last * (1 - c1) - c2 * sin(alpha_cur)) / (1 + c1)  # noqa:E731 using lambda

	if calculate_theoretical:
		__phi_beta_positive = lambda t: (alpha_start / 2 * ((1 + gamma / csqrt(beta)) * cexp((-gamma + csqrt(beta)) * t) + (1 - gamma / csqrt(beta)) * cexp((-gamma - csqrt(beta)) * t))).real  # noqa:E731 using lambda
		__phi_beta_negative_zero = lambda t: (alpha_start * cexp(-gamma * t) * (ccos(csqrt(-beta) * t) + gamma / csqrt(-beta) * csin(csqrt(-beta) * t))).real  # noqa:E731 using lambda

		get_theoretical_alpha = __phi_beta_positive if beta > 0 else __phi_beta_negative_zero

	for t in tqdm(time_array):  # main loop
		alpha_next = get_alpha(t)  # noqa:F823 - `get_alpha(...)` is always defined

		if calculate_theoretical:
			alpha_theoretical_next = get_theoretical_alpha(t)  # noqa:F823 - `get_theoretical_alpha(...)` is always defined
			theoretical_alpha_array.append(alpha_theoretical_next)

		alpha_last = alpha_cur
		alpha_cur = alpha_next

		alpha_array.append(alpha_next)

	with open(datapath, 'w') as f:  # noqa - datapath is always defined
		print(dt,                       file=f)  # exporting data to file
		print(l,                        file=f)
		print(t_max,                    file=f)
		print(n,                        file=f)
		print(*time_array,              file=f)
		print(*alpha_array,             file=f)
		print(*theoretical_alpha_array, file=f)
