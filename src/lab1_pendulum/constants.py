import logging
import os

from src.general.constants import *

__all__ = ["datapath_model", "datapath_input", "datapath_log", # output settings
           "plot_lims", "text_y", "figsize", "pendulum_axis_x", "pendulum_axis_y",  # noqa:typo, rendering settings
           ]


# output settings
datapath_model = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "data.dat")
datapath_input = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "input.ini")
datapath_log   = os.path.join(DATASTORE_ROOT, "lab1_pendulum", "log.log")

logging.basicConfig(
	filename=datapath_log,
    level=logging.INFO,
	format='%(asctime)s - %(levelname)s: %(message)s'
)


# rendering settings
plot_lims = 1.3  # xlim and ylim for a plot, divided by `l`
text_y = 1.0  # y coordinate of text with stopwatch
figsize = 7  # noqa:typo, size of the figure in inches
pendulum_axis_x = 0
pendulum_axis_y = 0
