from typing import NamedTuple, List
from pathlib import Path
import json

from plover.oslayer.config import CONFIG_DIR  # type: ignore

class Config(NamedTuple):
	command: List[str]
	escape_sequence_clear_window: str

CONFIGURATION_FILE_PATH=Path(CONFIG_DIR)/"textarea-config.json"

def load_config()->Config:
	text=CONFIGURATION_FILE_PATH.read_text() #might raise FileNotFoundError
	return Config(**json.loads(text))

