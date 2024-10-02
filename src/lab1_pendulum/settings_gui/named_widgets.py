from dataclasses import dataclass

__all__ = ['NamedLabelH2', 'NamedLabel', 'NamedLineEdit', 'NamedLabelUnit']


@dataclass
class NamedLabelH2:
	name: str
	text: str
	place: tuple[int, int]


@dataclass
class NamedLabel:
	name: str
	text: str
	place: tuple[int, int]
	hint: str = ""


@dataclass
class NamedLabelUnit:
	name: str
	text: str
	place: tuple[int, int]


@dataclass
class NamedLineEdit:
	name: str
	place: tuple[int, int]
	default: str = ""
