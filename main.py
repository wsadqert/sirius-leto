import os
import signal
import logging
import sys
import platform
import argparse
from rich.traceback import install
from rich.logging import RichHandler

from src.general.constants import *
from src.lab1_pendulum.constants import *

install(show_locals=True, width=300)  # will be removed in production

# parsing arguments
parser = argparse.ArgumentParser(description='lab1_pendulum')
parser.add_argument("-v", "--verbose", action="store_true", help="print logs to console")
args = parser.parse_args()


# configuring logger
logging.basicConfig(
	filename=datapath_log,
	filemode='w',
	level=logging.DEBUG,
	format='%(asctime)s - %(levelname)s: %(message)s'
)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
if args.verbose:
	logging.getLogger().addHandler(RichHandler())


# ctrl-c handler
def sigint_handler(signal, frame):
	msg = "Ctrl-C pressed, exiting..."
	logging.critical(msg)
	sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)  # noqa

# python version check
if platform.python_version_tuple()[:2] != ('3', '10'):
	msg = f"Python version check failed! Found incompatible version {''.join(platform.python_version_tuple())}, leaving"
	logging.critical(msg)
	raise OSError(msg)

# creating required folders
if not os.path.exists(DATASTORE_ROOT):
	print('creating DATASTORE_ROOT')
	os.mkdir(DATASTORE_ROOT)
if not os.path.exists(os.path.join(DATASTORE_ROOT, "lab1_pendulum")):
	os.mkdir(os.path.join(DATASTORE_ROOT, "lab1_pendulum"))

# adding project root to PYTHONPATH
sys.path.insert(1, PROJECT_ROOT)

from src.lab1_pendulum import start
if __name__ == '__main__':
	try:
		start()
	except Exception as e:
		logging.exception(e)
		raise
