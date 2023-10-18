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

	n: Final[int] = len(time_array)

	match mode:
		case "basic":
			get_alpha = lambda x: 2 * alpha_cur - alpha_last - k * sin(alpha_cur)  # noqa:E731 using lambda

		case "windage":
			k_windage = gamma * dt
			get_alpha = lambda x: (4 * alpha_cur - alpha_last * (2 - k_windage) - k * sin(alpha_cur)) / (2 + k_windage)  # noqa:E731 using lambda

		case "theoretical":
			def __phi_beta_positive(t: float) -> float:
				return (alpha_start / 2 * ((1 + gamma / csqrt(beta)) * cexp((-gamma + csqrt(beta)) * t) + (1 - gamma / csqrt(beta)) * cexp((-gamma - csqrt(beta)) * t))).real

			def __phi_beta_negative_zero(t: float):
				return (alpha_start * cexp(-gamma * t) * (ccos(csqrt(-beta) * t) + gamma / csqrt(-beta) * csin(csqrt(-beta) * t))).real

			get_alpha = __phi_beta_positive if beta > 0 else __phi_beta_negative_zero

	for t in tqdm(time_array):  # main loop
		alpha_next = get_alpha(t)  # noqa - datapath is always defined

		alpha_last = alpha_cur
		alpha_cur = alpha_next

		alpha_array.append(alpha_next)

	with open(datapath, 'w') as f:  # noqa - datapath is always defined
		print(dt,           file=f)  # exporting data to file
		print(l,            file=f)
		print(t_max,        file=f)
		print(n,            file=f)
		print(*time_array,  file=f)
		print(*alpha_array, file=f)
