#
# usbtmc.py
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

import usb.core
import usbtmc

from ..transport import *
from ..exceptions import *


class USBTMCDevice(SCPITransport):
    """
    USBTMCDevice class implmenes USBTMC transport using usbtmc module.
    """
    
    READ_BUF_SIZE = 1024*1024
    
    def __init__(self, device, timeout=5):
        """
        Open USBTMC device using usbtmc module.

        :device: connection string passed to usbtmc module
        :timeout: timeout for device to respond in seconds [Default 5 seconds]
        """
        
        self.conn = usbtmc.Instrument(device)

        
    def read(self):
        """
        Read data (reponse) from device.

        Returns the data excluding any trailing whitespace.
        """

        r = self.conn.read_raw(READ_BUF_SIZE)
        if self.verbose:
            print("%s: Read: '%s'" % (__name__, r))
        return r.rstrip()

    
    def write(self, data):
        """
        Write data (command) to device.
        """

        if self.verbose:
            print("%s: Write: '%s'" % (__name__, data))
        return selc.conn.write_raw(data)

        
