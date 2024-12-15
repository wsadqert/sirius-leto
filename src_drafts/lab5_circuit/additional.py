import math

def round_precision(value, precise):
	if precise == 0:
		return value

	exponent = math.floor(math.log10(abs(precise))) if precise != 0 else 0
	rounding_precision = 10 ** (exponent - 1)  # One order of magnitude more precise
	rounded_value = round(value / rounding_precision) * rounding_precision

	return round(rounded_value, -exponent)

