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
> ./split.py --help
usage: split.py [-v] [-d DEVICE] [-b BAUD] [-h]

A serial terminal in your browser.

optional arguments:
  -v, --version         Print version (default: False)
  -d DEVICE, --device DEVICE
                        Uart tty device (default: )
  -b BAUD, --baud BAUD  Uart baudrate (default: 115200)
  -h, --help            Print help (default: False)

```

# Reference

[pyxterm.js](https://github.com/cs01/pyxterm.js)
