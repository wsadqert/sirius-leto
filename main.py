from src.general.constants import *
from src.lab1_pendulum import start

sys.path.insert(1, PROJECT_ROOT)

start("windage", plot_animation=True, plot_alpha=True)
