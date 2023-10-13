from src.general.constants import *
import sys

sys.path.insert(1, PROJECT_ROOT)

from src.lab1_pendulum import start

start("windage", plot_animation=False, plot_alpha=True)
