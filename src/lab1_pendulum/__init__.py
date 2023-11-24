from pprint import pprint, pformat
import logging

from src.general.calculations import *
from .constants import *
from .gui import start_gui
from .model import model
from .animate import animate

__all__ = ["start"]


def start(is_verbose) -> None:
	"""
	Main function of `src.lab1_pendulum`.

	What it does:

	- clear screen

	- show gui

	- parse data from config file

	- start calculating model

	- render animation
	"""

	clear_screen()

	logging.info("Starting `Settings` window GUI...")
	config = start_gui()
	logging.debug('Get model configuration:\n' + pformat(config))

	model(config)
	logging.info("Model fully calculated")
	animate(is_verbose, config)  # drawing requested plots
