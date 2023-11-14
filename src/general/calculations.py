from math import sin, cos
from typing import Sequence
import numpy as np
from scipy.signal import argrelextrema

__all__ = ["clear_screen", "pol2cart", "find_extremums"]  # noqa:typo


def clear_screen():
	print("\x1B[H\x1B[J")


def pol2cart(r: float, phi: float) -> tuple[float, float]:
	"""
	Function that converts polar coordinates to cartesian.

	:return: Tuple of x and y coordinates.
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
