import os

from src.general.constants import DATASTORE_ROOT

__all__ = ["datapath_model", "datapath_log",  # output settings
           "plot_lims", "text_y", "figsize", "pendulum_axis_x", "pendulum_axis_y", "demo_duration",
           ]

# output settings
datapath_model = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "data.dat")
datapath_log   = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "last_run_log.log")


# rendering settings
plot_lims = 1.3  # xlim and ylim for a plot, divided by `l`
text_y = 1.0  # y coordinate of text with stopwatch
figsize = 7  # noqa:typo, size of the figure in inches
pendulum_axis_x = 0
pendulum_axis_y = 0
