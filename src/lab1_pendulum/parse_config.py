from configparser import ConfigParser

from src.lab1_pendulum.constants import *
from src.general.constants import *

__all__ = ["parse_config"]


def parse_config() -> dict[str, ...]:
	"""
	Parses the configuration file located at `datapath_input` and returns obtained data.

	:return: Dictionary with data, parsed from configuration file. The dictionary's keys are variable names, and values are variables' values.
	"""
	config = ConfigParser()
	config.read(datapath_input)

	ans = dict()

	for i in config.sections():
		current_section = config[i]

		for key, value in current_section.items():
			if key in ("mode", "windage_method"):  # read strings
				ans[key] = current_section.get(key)

			elif key in ("render_dt", "frames_count_fps"):  # parse integer
				ans[key] = current_section.getint(key)

			elif key in ("calculate_theoretical", "calculate_extremums", "plot_animation", "plot_alpha"):  # parse boolean
				ans[key] = current_section.getboolean(key)

			else:  # parse float
				ans[key] = current_section.getfloat(key)

	if ans['mode'] == 'basic':
		ans['k'] = 0

	# see README.md for description
	ans['gamma'] = ans['k'] / (2*ans['m'])
	ans['beta'] = ans['gamma']**2 - g / ans['l']
	ans['c1'] = ans['gamma'] * ans['dt']
	ans['c2'] = g * ans['dt'] ** 2 / ans['l']

	return ans
