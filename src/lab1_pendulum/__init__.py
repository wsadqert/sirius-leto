from pprint import pprint

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

	start_gui()
	config = parse_config()

	# REMOVE AFTER TESTING
	pprint(config, sort_dicts=False)
	# --------------------

	model(config)
	animate(config)  # drawing requested plots
