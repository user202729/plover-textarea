# plover-textarea

Display a text area that can be controlled from other plugins or strokes.

### Installation

This plugin can be installed from source on GitHub.

When it's released it can also be installed from PyPI (`pip install plover-textarea`)
or Plover's plugins manager.

### Note

You need to enable the extension plugin.

### Configuration

Currently only some UNIX systems/terminals (xterm) are supported. Qt GUI output is not supported.

You need to create a file `textarea-config.json` in Plover's configuration directory with the content:

```json
{
	"command": ["xterm", "-e", "cat /proc/$(echo $(ps -o ppid= $$))/fd/0"],
	"escape_sequence_clear_window": "\u001B[H\u001B[J"
}
```

### Usage

Define strokes like this

```json
{
"A": "{plover:textarea_write:a:b}",
"A": "{plover:textarea_write:a:text\n}",
"A": "{plover:textarea_clear:a}",
"A": "{plover:textarea_close:a}",
"...": "..."
}
```

`{}` should be escaped.

The value before the first `:` is the window name. Must be provided.

It's not possible to specify a window name that contains `:`, but it's possible in the Python API.

### Python API

Example code: (requires the extension plugin to be running)

```python
from plover_textarea.extension import get_instance

get_instance().write("a", "text to write\n")
get_instance().clear("a")
get_instance().close("a")
```
