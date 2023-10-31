import os
import sys
from time import sleep, time as real_time    # noqa: F401 - unused import

import matplotlib as mpl                     # noqa:F401 - unused import
import matplotlib.pyplot as plt              # noqa:F401 - unused import
import numpy as np                           # noqa:F401 - unused import
from tqdm import tqdm                        # noqa:F401 - unused import
from typing import Final, Literal, Iterable  # noqa:F401 - unused import

from scipy.constants import g                # noqa:F401 - unused import
from numpy import pi                         # noqa:F401 - unused import


PROJECT_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))
DATASTORE_ROOT = os.path.join(PROJECT_ROOT, "datastore")
