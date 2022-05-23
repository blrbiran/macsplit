#!/usr/bin/env python

import os
import sys
import serial
import time
import argparse
import threading

__version__ = "0.0.2.0"

class SerialSplit:
    def __init__(self, device="", baud=115200, op_channel=b"\x00"):
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
            print("Error open serial port: " + str(e))
            exit()
        self.gser = ser
        self.curChannel = b"\x00"
        self.channels = {self.curChannel: ""}
        self.logFds = {}
        self.opChannel = op_channel
        print("device: " + ser.port + ", baud: " + str(ser.baudrate))

        x = threading.Thread(target=self.thread_input, args=(1,))
        x.start()

    def thread_input(self, name):
        typeChannel = self.opChannel
        while True:
            in1 = input()
            self.gser.write(b"\xff" + typeChannel + bytearray(in1, "ascii") + b"\r")

    def printf(self, format, *args):
        sys.stdout.write(format % args)

    def do_split(self, bytes, encoding="ascii"):
        if bytes.find(b"\xff") == -1:
            self.channels[self.curChannel] += str(bytes, encoding=encoding)
        else:
            splitBytes = bytes.split(b"\xff")
            for chnBytes in splitBytes:
                if chnBytes == b"":
                    continue
                if chnBytes[0:1] in self.channels:
                    self.channels[chnBytes[0:1]] += str(chnBytes[1:], encoding=encoding)
                else:
                    self.channels[chnBytes[0:1]] = str(chnBytes[1:], encoding=encoding)
                self.curChannel = chnBytes[0:1]

    def byte_split(self, bytes, encoding="ascii"):
        try:
            self.do_split(bytes, encoding=encoding)
        except Exception as e:
            print("fail: " + str(e))
            # print(bytes)
            # print(bytes.hex())

    def saveLog(self, channel, content):
        if channel not in self.logFds:
            if not os.path.isdir("./log/"):
                os.mkdir("./log/")
            self.logFds[channel] = open("./log/log." + str(channel.hex()) + ".log", "a")
        self.logFds[channel].write(content)
        self.logFds[channel].flush()
        # print(self.logFds)

    def postProcess(self, printChannel):
        for channel, content in self.channels.items():
            if channel == printChannel:
                self.printf("%s", content)
            # Save log file
            self.saveLog(channel, content)
            self.channels[channel] = ""

    def serial_split(self, printChannel=b""):
        if printChannel == b"":
            printChannel = self.opChannel
        # encoding = "utf-8"
        encoding = "ascii"
        if self.gser.isOpen():
            try:
                self.gser.flushInput()   #flush input buffer, discarding all its contents
                self.gser.flushOutput()  #flush output buffer, aborting current output
                                    #and discard all that is in buffer

                time.sleep(0.5)   #give the serial port sometime to receive the data

                # gser.write(b"\xff\x30root\r\r\r")

                while True:
                    try:
                        response = self.gser.read(500)
                        # response = self.gser.read(5000)
                        # response = b"".join(gser.readlines())
                    except Exception as e:
                        response = b""
                    # print(response)
                    self.byte_split(response)
                    self.postProcess(printChannel)
                    # print(self.channels)

                self.gser.close()
            except Exception as e1:
                print("Error communicating...: " + str(e1))
        else:
            print("Cannot open serial port")

    def test_loopback(self):
        while True:
            in1 = input()
            print("$: " + in1)

    def test_send(self):
        while True:
            print("$: test")
            time.sleep(1)

    def test_dosplit(self):
        self.do_split(b"\xff\x30123\xff\x20321\xff\x01aaa")
        print(self.channels)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "A serial terminal in your browser. "
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    parser.add_argument("-v", "--version", action="store_true", help="Print version")
    parser.add_argument("-d", "--device", default="", help="Uart tty device")
    parser.add_argument("-b", "--baud", default="115200", help="Uart baudrate")
    parser.add_argument("-h", "--help", action="store_true", help="Print help")
    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit(0)
    if args.help:
        parser.print_help()
        exit(0)

    s = SerialSplit(args.device, int(args.baud), op_channel=b"\x30")
    s.serial_split()

    # s.test_loopback()
    # s.test_send()
    # s.test_dosplit()
