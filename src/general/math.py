from math import sin, cos

__all__ = ["pol2cart"]


def pol2cart(r: float, phi: float) -> tuple[float, float]:
	x = r * cos(phi)
	y = r * sin(phi)
	return x, y
