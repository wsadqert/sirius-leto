import signal
import logging
import sys

from rich.traceback import install
from src.general.constants import *
from src.lab1_pendulum import start

def signal_handler(signal, frame):
	logging.critical("Ctrl-C pressed, exiting...")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

install(show_locals=True, width=300)
sys.path.insert(1, PROJECT_ROOT)

start()
