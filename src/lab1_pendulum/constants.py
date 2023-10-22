from src.general.constants import *

__all__ = ["l", "alpha_start",  # physics settings
           "mode", "calculate_theoretical", "calculate_extremums", "dt", "t_max",  # model settings
           "datapath_basic", "datapath_windage", "datapath_theoretical",  # output settings
           "plot_lims", "text_y", "render_dt", "figsize", "pendulum_axis_x", "pendulum_axis_y", "frames_count_fps",  # noqa:typo, rendering settings
           "c1", "c2", "beta", "gamma",  # optimizations
           "MODE", "datapath",  # misc
           ]

# model settings
mode = "windage"  # Literal["basic", "windage"]
calculate_theoretical = True
calculate_extremums = True
dt: Final[float] = 1e-5
t_max: Final[float] = 10

# physics settings
l: Final[float] = g  # length of pendulum
alpha_start: Final[float] = -1.5  # * pi  # noqa:typo, initial angle of deviation of the pendulum from the equilibrium position
k = 0.7
m = 1

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
frames_count_fps = int(1e3)  # number of frames to count fps\

# optimizations

gamma = k / (2*m)  # air resistance coefficient
beta = gamma**2 - g/l

c1 = gamma * dt
c2 = g * dt ** 2 / l

if mode == 'basic':
	k = 0

# misc
MODE = Literal["basic", "windage"]
match mode:
	case "basic":
		datapath = datapath_basic
	case "windage":
		datapath = datapath_windage
	case _:
		datapath = ""
