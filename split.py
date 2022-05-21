#!/usr/bin/env python

import serial, time
import argparse
import threading

__version__ = "0.0.1.0"

def serial_init(device="", baud=115200):
    global gser
    # initialization and open the port

    # possible timeout values:
    #    1. None: wait forever, block call
    #    2. 0: non-blocking mode, return immediately
    #    3. x: x is bigger than 0, float allowed, timeout block call

    ser = serial.Serial()
    if device == "":
        # ser.port = "/dev/tty.usbmodem114203"
        # ser.port = "/dev/tty.usbmodem11201"
        ser.port = "/dev/tty.usbserial-0001"
    else:
        ser.port = device
    ser.baudrate = baud
    ser.bytesize = serial.EIGHTBITS     #number of bits per bytes
    ser.parity = serial.PARITY_NONE     #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  #number of stop bits
    # ser.timeout = None        #block read
    ser.timeout = 1             #non-block read
    # ser.timeout = 2            #timeout block read
    ser.xonxoff = False         #disable software flow control
    ser.rtscts = False          #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False          #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2        #timeout for write
    try:
        ser.open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()
    gser = ser
    print("device: " + device + ", baud: " + str(baud))

def thread_input(name):
    global gser
    while True:
        in1 = input()
        gser.write(b"\xff\x30" + bytearray(in1, "ascii") + b"\r")

def serial_split(channel=b"\x30"):
    global gser
    if gser.isOpen():
        try:
            gser.flushInput() #flush input buffer, discarding all its contents
            gser.flushOutput()#flush output buffer, aborting current output
                    #and discard all that is in buffer

            time.sleep(0.5)   #give the serial port sometime to receive the data

            # gser.write(b"\xff\x30root\r\r\r")
            encoding = "utf-8"
            encoding = "ascii"
            j = 0
            # i = 0
            while True:
                j += 1
                try:
                    # response = gser.read(1000)
                    response = b"".join(gser.readlines())
                except Exception as e:
                    # print(e)
                    response = b""
                # print(response)
                try:
                    res = str(response, encoding)
                    res = res.replace("\r", "")
                    res = res.replace("\n", "")
                    if res.isprintable():
                        # print("pass")
                        if response != b"":
                            # print(str(response))
                            print(response)
                    else:
                        print("fail")
                        print(response)
                        print(response.hex())
                        # print("".join(res.strip("\n")))
                except Exception as e:
                    print("fail")
                    print(response)
                    print(response.hex())

            gser.close()
        except Exception as e1:
            print("error communicating...: " + str(e1))
    else:
        print("cannot open serial port")

def test_loopback(device):
    while True:
        in1 = input()
        print("$: " + in1)

def test_send(device):
    while True:
        print("$: test")
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "A fully functional terminal in your browser. "
            "https://github.com/cs01/pyxterm.js"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    parser.add_argument("-v", "--version", action="store_true", help="Print version")
    parser.add_argument("-d", "--device", default="", help="Uart tty device")
    parser.add_argument("-b", "--baud", default="115200", help="Uart baudrate")
    parser.add_argument("-h", "--help", default="", help="Print help")
    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit(0)
    if args.help:
        parser.print_help()
        exit(0)

    serial_init(args.device, int(args.baud))
    x = threading.Thread(target=thread_input, args=(1,))
    x.start()
    serial_split()
    # test_loopback(args.device)
    # test_send(args.device)
