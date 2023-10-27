from rich.traceback import install

from src.general.constants import *
from src.lab1_pendulum import start
import src.lab1_pendulum.gui.gui

install(show_locals=True, width=300)

sys.path.insert(1, PROJECT_ROOT)

# start(plot_animation=True, plot_alpha=True)
