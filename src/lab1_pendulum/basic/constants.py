from src.general.constants import *

__all__ = ["l", "alpha_start",
           "dt", "t_max", "datapath",
           "plot_lims", "text_y", "render_dt", "figsize", "pendulum_axis_x", "pendulum_axis_y"]

# physics settings
l: Final[float] = 1  # length of pendulum
alpha_start: Final[float] = -0.99*pi  # initial angle of deviation of the pendulum from the equilibrium position


# model settings
dt: Final[float] = 1e-5
t_max: Final[float] = 15
datapath = os.path.join(PROJECT_ROOT, "datastore", "lab1_pendulum", "basic", "data.dat")

# rendering settings
plot_lims = 1.3  # xlim and ylim for plot, divided by `l`
text_y = 1.0  # y coordinate of text with stopwatch
render_dt = 500
figsize = 7  # size of the figure in inches
pendulum_axis_x = 0
pendulum_axis_y = 0
frames_count = int(1e3)  # number of frames to count fps
