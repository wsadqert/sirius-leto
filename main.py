import os
import signal
import logging
import sys
import platform
from rich.traceback import install

from src.general.constants import *
from src.lab1_pendulum.constants import *

install(show_locals=True, width=300)  # will be removed in production

# configuring logger
logging.basicConfig(
	filename=datapath_log,
	filemode='w',
    level=logging.DEBUG,
	format='%(asctime)s - %(levelname)s: %(message)s'
)
logging.getLogger('matplotlib').setLevel(logging.WARNING)


# ctrl-c handler
def sigint_handler(signal, frame):
	msg = "Ctrl-C pressed, exiting..."
	print(msg)
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
