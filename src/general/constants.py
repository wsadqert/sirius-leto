import os
import sys
from time import sleep, time as real_time    # noqa: F401 - unused import

from typing import Final, Literal, Iterable, Sequence  # noqa:F401 - unused import

from scipy.constants import g                # noqa:F401 - unused import
from numpy import pi                         # noqa:F401 - unused import


PROJECT_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))
DATASTORE_ROOT = os.path.join(PROJECT_ROOT, "datastore")

__all__ = ["PROJECT_ROOT", "DATASTORE_ROOT", "real_time", "Final", "Literal", "Iterable", "Sequence", "g", "pi"]
