import logging
import sys


def clear_screen():
	print("\x1B[H\x1B[J")


def sigint_handler(signal, frame):
	msg = "Ctrl-C pressed, exiting..."
	logging.critical(msg)
	sys.exit(0)
