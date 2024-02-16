import logging
import sys
from types import TracebackType
from typing import Optional

from rich.console import Console
from rich.traceback import Traceback


def clear_screen():
	print("\x1B[H\x1B[J")


def sigint_handler(_signal, _frame):
	msg = "Ctrl-C pressed, exiting..."
	logging.critical(msg)
	sys.exit(0)


def rich_excepthook(_event, _type: type[BaseException], value: BaseException, traceback: Optional[TracebackType]) -> None:
	Console(stderr=True).print(
		Traceback.from_exception(
			_type,
			value,
			traceback,
			width=300,
			extra_lines=3,
			theme=None,
			word_wrap=False,
			show_locals=False,
			locals_max_length=10,
			locals_max_string=80,
			locals_hide_dunder=True,
			locals_hide_sunder=bool(None),
			indent_guides=True,
			suppress=(),
			max_frames=100,
		)
	)
