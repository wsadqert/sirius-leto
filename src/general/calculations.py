from math import sin, cos
from typing import Sequence
import numpy as np
from scipy.signal import argrelextrema

__all__ = ["pol2cart", "find_minimums", "find_maximums", "find_extremums", "sign"]  # noqa:typo


def pol2cart(r: float, phi: float) -> tuple[float, float]:
	"""
	Function that converts polar coordinates to cartesian.

	:param r: The radial distance from the origin in the polar coordinate system.
	:param phi: The angle in radians from the positive x-axis in the polar coordinate system.
	:return: A tuple containing the x and y coordinates in the cartesian coordinate system.
	"""
	x = r * cos(phi)
	y = r * sin(phi)
	return x, y


def find_minimums(data: Sequence) -> tuple | np.ndarray:
	"""
	Finds all local minimums in 1d-array `data`.

	:param data: Array in which to find the relative minimums.
	:return: Indices of the minimums in `data`.
	"""
	return argrelextrema(np.array(data), np.less)[0]


def find_maximums(data: Sequence) -> tuple | np.ndarray:
	"""
	Finds all local maximums in 1d-array `data`.

	:param data: Array in which to find the relative maximums.
	:return: Indices of the maximums in `data`.
	"""
	return argrelextrema(np.array(data), np.greater)[0]


def find_extremums(data: Sequence) -> np.ndarray:  # noqa:typo
	"""
	Finds all local extremums in 1d-array `data`.

	:param data: Array in which to find the relative extrema.
	:return: Indices of the extremums in `data`.
	"""
	return np.array([*set(find_minimums(data)) | set(find_maximums(data))])


def sign(x: float):
	if x < 0:    return -1
	elif x == 0: return 0
	else:        return 1
