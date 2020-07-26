#
# tcp.py
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
import socket
import select

from ..transport import *
from ..exceptions import *

class TCPDevice(SCPITransport):
    """
    TCPDevice class implmeents TCP/IP transport.
    """
    
    READ_BUF_SIZE = 1024*1024
    DEFAULT_PORT = 5555
    
    def __init__(self, device, port, timeout=5):
        """
        Open TCP connection to specified device.

        :device: Target device hostname or IP address.
        :port: Target device TCP port.
        :timeout: Timeout for device to respond in seconds [Default: 5 seconds]
        """
        if (port == None):
            self.port = DEFAULT_PORT
        else:
            self.port = port
        self.host = device
        self.timeout = timeout
            
        try:
            self.conn = socket.create_connection((self.host, self.port), timeout)
        except (ConnectionRefusedError, socket.gaierror, socket.timeout) as err:
            errmsg = "Connection to %s:%s failed: %s" % (self.host, self.port, err)
            raise SCPITransportError(errmsg)

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass

    def read(self):
       """
        Read data (reponse) from device.

        Returns the data excluding any trailing whitespace.
        """
         
        try:
            r = self.conn.recv(self.READ_BUF_SIZE)
        except socket.timeout:
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
        return self.conn.sendall(data)

        
