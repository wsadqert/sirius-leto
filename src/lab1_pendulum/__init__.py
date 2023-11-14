from pprint import pprint
import logging

from src.general.calculations import *
from .constants import *
from .gui import start_gui
from .parse_config import parse_config
from .model import model
from .animate import animate

__all__ = ["start"]


def start() -> None:
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
	start_gui()
	logging.info(f"Parsing config file {datapath_input}...")
	config = parse_config()

	# REMOVE AFTER TESTING
	pprint(config, sort_dicts=False)
	# --------------------

	logging.info("Calculating model...")
	model(config)
	logging.info("Rendering animation...")
	animate(config)  # drawing requested plots
