from src.general.constants import *

__all__ = ["contains_one_of", "is_one_of", "is_float", "is_not_nan_inf", "is_non_negative"]


def contains_one_of(string: str, substring_list: Iterable) -> bool:
	"""Checks if string contains one of `substring_list`"""
	return any(map(string.__contains__, substring_list))  # the fastest way presented here https://stackoverflow.com/a/8122096


def is_one_of(data, possible_values) -> bool:
	return any(map(data.__eq__, possible_values))


def is_float(element) -> bool:
	# If you expect None to be passed:
	if element is None:
		return False

	try:
		if isinstance(element, str):
			if '_' in element:
				return False

		float(element)
		return True
	except (ValueError, TypeError):
		return False


def is_not_nan_inf(element) -> bool:
	return is_float(element) and not is_one_of(float(element), (float('nan'), float('inf'), float('-inf')))


def is_non_negative(element) -> bool:
	return is_float(element) and float(element) != 0
