import os
import sys
from time import sleep, time as real_time

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from typing import Final, Literal

from scipy.constants import g
from numpy import pi

PROJECT_ROOT = os.path.dirname(sys.argv[0])
DATASTORE_ROOT = os.path.join(PROJECT_ROOT, "datastore")
