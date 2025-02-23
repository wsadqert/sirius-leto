__all__ = ["u"]

class Units:
	"""
	A simplified units module with decimal prefixes and aliases.
	"""
	# Define decimal prefixes, their multipliers, and aliases
	PREFIXES = {
		'Y': {'multiplier': 1e24, 'aliases': ['yotta']},
		'Z': {'multiplier': 1e21, 'aliases': ['zetta']},
		'E': {'multiplier': 1e18, 'aliases': ['exa']},
		'P': {'multiplier': 1e15, 'aliases': ['peta']},
		'T': {'multiplier': 1e12, 'aliases': ['tera']},
		'G': {'multiplier': 1e9, 'aliases': ['giga']},
		'M': {'multiplier': 1e6, 'aliases': ['mega']},
		'k': {'multiplier': 1e3, 'aliases': ['kilo']},
		'h': {'multiplier': 1e2, 'aliases': ['hecto']},
		'da': {'multiplier': 1e1, 'aliases': ['deca']},
		'': {'multiplier': 1e0, 'aliases': ['base']},
		'd': {'multiplier': 1e-1, 'aliases': ['deci']},
		'c': {'multiplier': 1e-2, 'aliases': ['centi']},
		'm': {'multiplier': 1e-3, 'aliases': ['milli']},
		'µ': {'multiplier': 1e-6, 'aliases': ['micro']},
		'n': {'multiplier': 1e-9, 'aliases': ['nano']},
		'p': {'multiplier': 1e-12, 'aliases': ['pico']},
		'f': {'multiplier': 1e-15, 'aliases': ['femto']},
		'a': {'multiplier': 1e-18, 'aliases': ['atto']},
		'z': {'multiplier': 1e-21, 'aliases': ['zepto']},
		'y': {'multiplier': 1e-24, 'aliases': ['yocto']}
	}

	def __init__(self):
		# Create attributes for all prefixes and their aliases
		for prefix, data in self.PREFIXES.items():
			multiplier = data['multiplier']
			aliases = data['aliases']

			# Set the prefix as an attribute
			setattr(self, prefix, multiplier)

			# Set aliases as attributes pointing to the same multiplier
			for alias in aliases:
				setattr(self, alias, multiplier)

	def __rmul__(self, value):
		"""
		Multiply a value by a unit (e.g., 5 * u.kilo).
		:param value: The value to multiply.
		:return: The scaled value (int or float).
		"""
		if isinstance(value, (int, float)):
			return value * self.multiplier
		raise TypeError(f"Cannot multiply {type(value)} with Units")


u = Units()
