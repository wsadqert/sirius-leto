from src.general.constants import *

__all__ = ["l", "alpha_start",
           "dt", "t_max", "datapath",
           "plot_lims", "text_y", "render_dt", "figsize", "pendulum_axis_x", "pendulum_axis_y"]

# physics settings
l: Final[float] = 1
alpha_start: Final[float] = -0.99*pi


# model settings
dt: Final[float] = 1e-5
t_max: Final[float] = 15
datapath = os.path.join(PROJECT_ROOT, "datastore", "lab1_pendulum", "basic", "data.dat")

# rendering settings
plot_lims = 1.3
text_y = 1.0
render_dt = 500
figsize = 7
pendulum_axis_x = 0
pendulum_axis_y = 0
frames_count = int(1e3)  # number of frames to count fps
