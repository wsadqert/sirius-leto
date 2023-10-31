from src.general.constants import *

__all__ = ["datapath_model", "datapath_input",  # output settings
           "plot_lims", "text_y", "figsize", "pendulum_axis_x", "pendulum_axis_y",  # noqa:typo, rendering settings
           "MODE",  # misc
           ]

# output settings
datapath_model = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "data.dat")
datapath_input = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "input", "data.ini")


# rendering settings
plot_lims = 1.3  # noqa:typo, xlim and ylim for plot, divided by `l`
text_y = 1.0  # y coordinate of text with stopwatch
figsize = 7  # noqa:typo, size of the figure in inches
pendulum_axis_x = 0
pendulum_axis_y = 0


# misc
MODE = Literal["basic", "windage"]
