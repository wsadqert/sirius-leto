import os
import sys
from time import perf_counter, time as real_time       # noqa: F401 - unused import

from scipy.constants import g                          # noqa:F401 - unused import
from numpy import pi                                   # noqa:F401 - unused import

__all__ = ["PROJECT_ROOT", "DATASTORE_ROOT", "ASSETS_ROOT", "sleep", "real_time", "g", "pi", "sleep"]

PROJECT_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))
DATASTORE_ROOT = os.path.join(PROJECT_ROOT, "datastore")
ASSETS_ROOT = os.path.join(PROJECT_ROOT, "assets")


def sleep(duration):
	now = perf_counter()
	end = now + duration
	while now < end:
		now = perf_counter()
