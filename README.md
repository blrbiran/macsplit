# SerialSplitter

A serial console terminal in your browser. Tool fork from pyxterm.js

## Installation

```bash
pip install -r requirements.txt
python pyxtermjs/app.py -d /dev/tty.usbserial-0001 -b 115200
open http://localhost:5005
```

## API
```bash
> split.py --help
usage: pyxtermjs [-h] [-p PORT] [--host HOST] [--debug] [--version]
                 [--command COMMAND] [--cmd-args CMD_ARGS]

A fully functional terminal in your browser.
https://github.com/cs01/pyxterm.js

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to run server on (default: 5000)
  --host HOST           host to run server on (use 0.0.0.0 to allow access
                        from other hosts) (default: 127.0.0.1)
  --debug               debug the server (default: False)
  --version             print version and exit (default: False)
  --command COMMAND     Command to run in the terminal (default: bash)
  --cmd-args CMD_ARGS   arguments to pass to command (i.e. --cmd-args='arg1
                        arg2 --flag') (default: )
```

# Reference

[pyxterm.js](https://github.com/cs01/pyxterm.js)
