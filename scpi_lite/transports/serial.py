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
    
    def __init__(self, device, timeout=5, terminator=b'\n',
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
        self.conn.flush()
        self.terminator = terminator


    def read(self):
        """
        Read data (reponse) from device.
        Read until response trerminator received (default: \n).

        Returns the data up to the terminator.
        """
        buf = bytearray()
        while True:
            r = self.conn.read(1)
            if (len(r) < 1):
                break
            if self.verbose:
                print('Received: %s' % (r))
            buf.extend(r)
            if (buf.endswith(self.terminator)):
                buf = buf.rstrip(self.terminator)
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
        return self.conn.write(data)

