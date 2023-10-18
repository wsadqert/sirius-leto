from src.general.constants import *

__all__ = ["l", "alpha_start", "gamma",  # physics settings
           "mode", "calculate_theoretical", "dt", "t_max",  # model settings
           "datapath_basic", "datapath_windage", "datapath_theoretical",  # output settings
           "plot_lims", "text_y", "render_dt", "figsize", "pendulum_axis_x", "pendulum_axis_y", "frames_count",  # noqa:typo, rendering settings
           "k", "beta",  # optimizations
           "MODE", "datapath",  # misc
           ]

# model settings
mode = "windage"
calculate_theoretical = True
dt: Final[float] = 1e-5
t_max: Final[float] = 7

# physics settings
l: Final[float] = 1  # length of pendulum
alpha_start: Final[float] = -0.001  # * pi  # noqa:typo, initial angle of deviation of the pendulum from the equilibrium position
gamma = 0.1     # air resistance coefficient

# output settings
datapath_basic = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "basic", "data.dat")
datapath_windage = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "windage", "data.dat")
datapath_theoretical = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "theoretical", "data.dat")

# rendering settings
plot_lims = 1.3  # noqa:typo, xlim and ylim for plot, divided by `l`
text_y = 1.0  # y coordinate of text with stopwatch
render_dt = 500
figsize = 7  # noqa:typo, size of the figure in inches
pendulum_axis_x = 0
pendulum_axis_y = 0
frames_count = int(1e3)  # number of frames to count fps

# optimizations
if mode == 'basic':
	gamma = 0
k: Final[float] = g * dt ** 2 / l
beta = gamma**2 - g/l

# misc
MODE = Literal["basic", "windage", "theoretical"]
match mode:
	case "basic":
		datapath = datapath_basic
	case "windage":
		datapath = datapath_windage
	case "theoretical":
		datapath = datapath_theoretical
