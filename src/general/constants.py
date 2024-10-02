import os
import sys
from time import perf_counter, time as real_time       # noqa: F401 - unused import

from scipy.constants import g                          # noqa:F401 - unused import
from math import pi                                   # noqa:F401 - unused import

PROJECT_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))
DATASTORE_ROOT = os.path.join(PROJECT_ROOT, "datastore")
ASSETS_ROOT = os.path.join(PROJECT_ROOT, "assets")
IMAGES_ROOT = os.path.join(ASSETS_ROOT, "images")
ICONS_ROOT = os.path.join(IMAGES_ROOT, "icons")

BIBLIOGRAPHY = os.path.join(ASSETS_ROOT, "bibliography.txt")
QLISTVIEW_STYLE = os.path.join(ASSETS_ROOT, "QListView.css")


def sleep(duration: float):
	now = perf_counter()
	end = now + duration
	while now < end:
		now = perf_counter()
