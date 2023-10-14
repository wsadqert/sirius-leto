from math import sin, cos
from typing import Sequence
import numpy as np
from scipy.signal import argrelextrema

__all__ = ["pol2cart", "find_extremum"]


def pol2cart(r: float, phi: float) -> tuple[float, float]:
	"""
	Function that converts polar coordinates to cartesian.

	:return: Tuple of x and y coordinates.
	"""
	x = r * cos(phi)
	y = r * sin(phi)
	return x, y


def find_extremum(data: Sequence, comparator) -> tuple | np.ndarray:
	"""
	Finds the first local extremum id 1d-array `data`.

	:param comparator: Function to use to compare two data points. Should take two arrays as arguments.
	:param data: Array in which to find the relative extrema.
	:return: Indices of the maxima in `data`.
	"""
	return argrelextrema(np.array(data), np.greater)[0]
