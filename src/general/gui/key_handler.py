from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


def _handle_key_gen(key: int, handler: Callable):
	print(f"gen {key}, {Qt.Key(key).name}, {handler}")
	def _handle_key(_event: QKeyEvent):
		print(_event.key())
		print(Qt.Key(_event.key()).name)
		if _event.key() == key:
			handler()

	return _handle_key
