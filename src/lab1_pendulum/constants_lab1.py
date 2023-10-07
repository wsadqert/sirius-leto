from general.constants import *

__all__ = ["dt", "l", "t_max", "alpha_start", "datapath", "plot_lims", "text_y", "render_dt", "figsize", "pendulum_axis_x", "pendulum_axis_y"]

dt: Final[float] = 1e-5
l: Final[float] = 1
t_max: Final[float] = 5
alpha_start: Final[float] = 1

datapath = os.path.join(PROJECT_ROOT, "datastore", "lab1_pendulum", "data.dat")
plot_lims = 1.3
text_y = 1.0
render_dt = 500
figsize = 7

pendulum_axis_x = 0
pendulum_axis_y = 0
