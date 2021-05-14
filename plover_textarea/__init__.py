from .extension import get_instance

def write_command(engine, argument: str)->None:
	window, text=argument.split(":", maxsplit=1)
	get_instance().write(window, text)

def clear_command(engine, argument: str)->None:
	window=argument
	get_instance().clear(window)

def close_command(engine, argument: str)->None:
	window=argument
	get_instance().close(window)
