from dataclasses import dataclass

__all__ = ["DrawerConfig"]

@dataclass
class DrawerConfig:
	ray_width: int = 1
	ray_color: str = "white"

	source_size: int = 1
	source_color: str = "white"
	source_outline_color: str = "white"

	lens_width: int = 1
	lens_color: str = "white"

	mirror_width: int = 1
	mirror_color: str = "white"

	# get dict with non-None values
	def __post_init__(self):
		# self.__dict__ = {key: value for key, value in self.__dict__.copy().items() if value is not None}
		
		self.ray_width = int(self.ray_width)
		self.source_size = int(self.source_size)
		self.lens_width = int(self.lens_width)
		self.mirror_width = int(self.mirror_width)
