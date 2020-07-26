#
# linux_usbtmc.py
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

from ..transport import *
from ..exceptions import *

class LinuxUSBTMCDevice(SCPITransport):
    """
    LinuxUSBTMCDevice class implements Linux USBTMC driver transport.

    This works with /dev/usbtmc* devices present on a Linux system.
    """

    READ_BUF_SIZE = 1024*1024

    def __init__(self, device, timeout=5, verbose=False):
        """
        Open USBTMC device (/dev/usbtmc*) based connection.

        :device: device name (/dev/usbtmc0, ...)
        :timeout: timeout for device to respond in seconds [Default 5 seconds]
        """

        try:
            self.conn = os.open(device, os.O_RDWR)
        except OSError as err:
            raise SCPITransportError(err)

        self.timeout = timeout
        self.verbose = verbose


    def __del__(self):
        try:
            os.close(self.conn)
        except:
            pass


    def read(self):
        """
        Read data (reponse) from device.

        Returns the data excluding any trailing whitespace.
        """

        try:
            r = os.read(self.conn, self.READ_BUF_SIZE)
        except TimeoutError:
            print('%s: read timeout' % (__name__))
            r = bytes()
        if self.verbose:
            print('Read: %d: %s' % (len(r), r))
        return r.rstrip()


    def write(self, data):
        """
        Write data (command) to device.
        """

        if self.verbose:
            print('Write: %d: %s' % (len(data), data))
        return os.write(self.conn, data)

        
