from configparser import ConfigParser

def parse_config(filename: str) -> ConfigParser:
	config = ConfigParser()
	config.read(filename)

	return config
