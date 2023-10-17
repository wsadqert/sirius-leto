from rich.traceback import install
from src.general.constants import *
from src.lab1_pendulum import start

install(show_locals=True, width=300)

sys.path.insert(1, PROJECT_ROOT)

start("windage", plot_animation=True, plot_alpha=True)
