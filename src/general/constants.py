import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from rich.console import Console
from typing import Final

from scipy.constants import *
from numpy import pi

rich_console = Console()

PROJECT_ROOT = os.path.dirname(sys.argv[0])
