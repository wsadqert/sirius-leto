from pprint import pprint

from src.general.calculations import *
from .gui import start_gui
from .parse_config import parse_config
from .model import model
from .animate import animate

__all__ = ["start"]


def start() -> None:
	"""
	Wrapper for `src.lab1_pendulum.animate.animate(…)`.

	:return: None.
	"""

	clear_screen()

	start_gui()
	config = parse_config()

	# REMOVE AFTER TESTING
	pprint(config, sort_dicts=False)
	# --------------------

	model(config)
	animate(config)  # drawing requested plots
