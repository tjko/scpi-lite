#
# serial.py
#
# This file is part of scpi_lite python library.
#
# Copyright (C) 2020 Timo Kokkonen <tjko@iki.fi>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import serial

from ..transport import *
from ..exceptions import *


class SerialDevice(SCPITransport):
    """
    SerialDevice class implements Serial (RS-232/TTL) transport.
    """

    def __init__(self, device, timeout=5, terminator=(b'\r\n', b'\n'), verbose=0,
                 baudrate=115200, bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 xonxoff=False, rtscts=False, dsrdtr=False):
        """
        Open serial connection to specified device.

        :device: string specifying serial port (/dev/tty*, COM1:, ...)
        :timeout: timeout for device to respond in seconds [Default: 5 seconds]
        :baudrate: baudrate [Default: 115200]
        :bytesize: byte size [Default: EIGHTBITS]
        :parity: parity [Default: NONE]
        :stopbits: stop bits [Default: STOPBITS_ONE]
        :xonxoff: use XON/XOFF flow control [Default: False]
        :rtscts: use RTS/CTS flow control [Default: False]
        :dsrdtr: use DSR/DTR flow control [Default: False]
        """

        try:
            self.conn = serial.Serial(port=device, baudrate=baudrate, bytesize=bytesize,
                                      parity=parity, stopbits=stopbits, timeout=timeout,
                                      xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr)
        except (OSError, ValueError, serial.SerialException) as err:
            raise SCPITransportError(err)

        self.terminator = terminator
        self.verbose = verbose


    def read(self):
        """
        Read data (reponse) from device.
        Read until response trerminator received (default: \r\n or \n).

        Returns the data up to the terminator.
        """
        buf = bytearray()
        while True:
            try:
                r = self.conn.read(1)
            except serial.SerialException as err:
                raise SCPITransportError(err)
            if (len(r) < 1):
                break
            if self.verbose > 1:
                print('Received: %s' % (r))
            buf.extend(r)
            endofline = 0
            for term in self.terminator:
                if (buf.endswith(term)):
                    buf = buf.rstrip(term)
                    endofline = 1
                    break
            if endofline:
                break

        buf = bytes(buf)
        if self.verbose:
            print('Read: %d: %s' % (len(buf), buf))
        return buf

    def write(self, data):
        """
        Write data (command) to device.
        """
        if self.verbose:
            print('Write: %d: %s' % (len(data), data))
        try:
            res = self.conn.write(data)
        except serial.SerialException as err:
            raise SCPITransportError(err)
        return res

    def flush_input(self):
        """
        Flush serial input buffer.
        """
        if self.verbose:
            print("Flush serial input buffer.")
        self.conn.reset_input_buffer()

    def flush_output(self):
        """
        Flush serial output buffer.
        """
        if self.verbose:
            print("Flush serial input buffer.")
        self.conn.reset_output_buffer()

    def pending_input(self):
        """
        Return number of bytes waiting in input buffer.
        """
        return self.conn.in_waiting

    def close(self):
        """
        Close serial connection.
        """
        return self.conn.close()
