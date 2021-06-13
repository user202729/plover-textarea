import subprocess
from typing import Optional, Dict

from .config import load_config

class Main:
	def __init__(self, engine)->None:
		pass

	def start(self)->None:
		global instance
		self._config=load_config()
		assert instance is None
		instance=self
		# note: is the race condition problematic?

		self._process: Dict[str, subprocess.Popen]={}

	def stop(self)->None:
		global instance
		assert instance is self
		instance=None

		while self._process:
			window=next(iter(self._process.keys()))
			self.close(window)

	def start_process(self, window: str)->None:
		assert window not in self._process
		self._process[window]=subprocess.Popen(self._config.command, stdin=subprocess.PIPE)

	def _write_internal(self, window: str, text: str, retry: bool=True)->None:
		if window not in self._process:
			self.start_process(window)
		try:
			pipe=self._process[window].stdin
			assert pipe
			pipe.write(text.encode("UTF-8"))
			pipe.flush()
		except BrokenPipeError:
			if not retry: raise  # avoid infinite loop (if any)
			self.close(window)
			self._write_internal(window, text, retry=False)

	def write(self, window: str, text: str)->None:
		# is it necessary to lock this?
		self._write_internal(window, text)

	def clear(self, window: str)->None:
		self.write(window, self._config.escape_sequence_clear_window)

	def close(self, window: str)->None:
		if window not in self._process:
			return
		try:
			pipe=self._process[window].stdin
			assert pipe
			pipe.close()
		except BrokenPipeError:
			pass
		self._process[window].wait(timeout=1)  # might raise subprocess.TimeoutExpired
		del self._process[window]

instance: Optional[Main]=None

def get_instance()->Main:
	instance_=instance #avoid race conditions
	if instance_ is None: raise RuntimeError("Extension plugin is not running!")
	return instance_
