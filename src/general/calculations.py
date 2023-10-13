from math import sin, cos
import numpy as np
from scipy.signal import argrelextrema

__all__ = ["pol2cart", "find_extremum"]


def pol2cart(r: float, phi: float) -> tuple[float, float]:
	"""
	Function to convert polar coordinates to cartesian.

	:return: tuple of x and y coordinates.
	"""
	x = r * cos(phi)
	y = r * sin(phi)
	return x, y


def find_extremum(data):
	return argrelextrema(np.array(data), np.greater)[0][0]
