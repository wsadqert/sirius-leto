from typing import Iterable, Sequence

__all__ = ["contains_one_of", "check_type_convertible", "is_convertible", "is_not_nan_inf", "is_positive", "is_not_negative"]


def contains_one_of(string: Sequence, substring_list: Iterable) -> bool:
	"""
	Checks if object `string` contains one of `substring_list`.

	For example:

	>>> contains_one_of('abracadabra', ['abr', 'w', 'p'])
	>>> True

	>>> contains_one_of('abracadabra', ['f', 'v', 'n'])
	>>> False

	:param string: object (not necessarily a string) for which you need to check occurrences of objects from `substring_list`
	:param substring_list: object, an iterable collection of objects whose occurrences need to be checked

	"""
	return any(map(string.__contains__, substring_list))  # the fastest way. Presented here https://stackoverflow.com/a/8122096


def check_type_convertible(element: any, new_type: type) -> bool:
	"""
	Checks if object `element` is convertible to type `new_type`.

	For example:

	>>> check_type_convertible('0.001', float)
	>>> True

	>>> check_type_convertible({}, int)
	>>> False

	:param element: object to check.
	:param new_type: type to which the object `object` should be cast.
	:return: boolean value, indices the ability to cast the `object` to type `new_type`.

	"""
	# If you expect None to be passed:
	if element is None:
		return False

	try:
		new_type(element)
		return True
	except (ValueError, TypeError):
		return False


is_convertible = check_type_convertible


def is_not_nan_inf(element: any) -> bool:
	"""
	Tries to cast `element` to float and checks if it is not in (±inf, nan).

	For example:

	>>> is_not_nan_inf('0.001')
	>>> True

	>>> is_not_nan_inf(['q', 'w'])
	>>> False

	:param element: object to check.
	:return: boolean value, indices the ability to cast the `element` to float and `float(element)` is not in (±inf, nan).

	"""
	return (check_type_convertible(element, float) and
	        float(element) not in (float('nan'), float('inf'), float('-inf')))


def is_positive(element: any) -> bool:
	"""
	Similar to `is_not_nan_inf`.
	Tries to cast `element` to `float` and checks if it is positive (greater than 0).

	For example:

	>>> is_not_nan_inf('0.001')
	>>> True

	>>> is_not_nan_inf(['q', 'w'])
	>>> False

	:param element: object to check
	:return: boolean value, indices the ability to cast the `element` to `float` and `float(element)` is positive.
	"""
	return is_not_nan_inf(element) and float(element) > 0


def is_not_negative(element: any) -> bool:
	"""
	Similar to `is_not_nan_inf`.
	Tries to cast `element` to `float` and checks if it is positive (greater than 0).

	For example:

	>>> is_not_nan_inf('0.001')
	>>> True

	>>> is_not_nan_inf(['q', 'w'])
	>>> False

	:param element: object to check
	:return: boolean value, indices the ability to cast the `element` to `float` and `float(element)` is positive.
	"""
	return is_not_nan_inf(element) and float(element) >= 0
