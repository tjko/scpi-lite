#
# scpi.py 
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

import importlib
import re
import time

from .exceptions import *


def load_transport(name):
    """Helper function to load transport backends at runtime."""
    try:
        module = importlib.import_module('scpi_lite.transports.' + name)
    except ImportError as e:
        raise SCPITransportError(e)
    return module


class SCPIDevice(object):
    """
    SCPIDevice class reporesents a SCPI device (instrument).

    This class allows sending arbitrary commands/queries to device.
    Underlying connection to device (serial, TCP/IP, etc...) is handled
    by the SCPITransport class.
    """
    conn = None
    encoding = None
    command_terminator = None
    verbose = False
    quirk_no_idn = False
    quirk_no_opc = False
    quirk_no_syst_err = False
    no_opc_delay = 0.25
    manufacturer = 'Unknown'
    model = 'Unknown'
    serial = 'Unknown'
    firmware = 'Unknown'
    idn = ''
    last_error = ''


    def __init__(self, device, command_terminator='\n',
                 idn=True, opc=True, err=True,
                 encoding='utf-8', **args):
        """
        Creates an instance of SCPIDevice to commmunicate with instruments.

        :device: Connection string identifying the device to connect to.
        :idn: Device supports *IDN? command (True/False). [Default: True]
        :opc: Device supports *OPC? command (True/False). [Default: True]
        :err: Device support SYST:ERR? command (True/False). [Default: True]

        Additionally transport specific options can be added that are passed
        directly to underlying transport class (SCPITransport).
        """
        m = re.match(r'^\s*(?P<device>\S+?)(\s*:\s*(?P<port>\S+))?\s*$', device)
        if m:
            dev = m.group('device')
            port = m.group('port')
            if dev == 'USB':
                transport = load_transport('usbtmc')
                conn = transport.USBTMCDevice(device, **args)
            elif port:
                transport = load_transport('tcp')
                conn = transport.TCPDevice(dev, port, **args)
            elif (dev.startswith("/dev/usbtmc")):
                transport = load_transport('linux_usbtmc')
                conn = transport.LinuxUSBTMCDevice(dev, **args)
            else:
                transport = load_transport('serial')
                conn = transport.SerialDevice(dev, **args)
        else:
            raise SCPIError("Invalid device string: '%s'" % (device))

        self.conn = conn
        self.encoding = encoding
        self.command_terminator = command_terminator
        self.quirk_no_idn = not idn
        self.quirk_no_opc = not opc
        self.quirk_no_syst_err = not err

        if (self.unit_ready() != 1):
            raise SCPIError("No response (Not SCPI compatible device?): %s" % (device))

        if self.quirk_no_idn:
            return

        res = self._idn()
        if res:
            if self.verbose:
                print('IDN: %s' % (res))
            self.idn = res
            i = res.split(',')
            if (len(i) < 2):
                raise SCPIError("Invalid IDN response: '%s'" % (res))
            self.manufacturer = i[0]
            self.model = i[1]
            if (len(i) < 4):
                self.serial='Unknown'
                self.firmware=i[2]
            else:
                self.serial = i[2]
                self.firmware = i[3]
        else:
            raise SCPIError("No response to *IDN? (not SCPI compliant device?): %s" % (device))
        self._cls()



    def write(self, cmd):
        """
        Send an arbitrary string to device. If string is not terminated with a
        command terminator (default: \n), it will be added automatically.

        This function expects a string argument that is encoded to bytes.
        """
        if self.verbose:
            print('%s: write: %s' % (__name__, cmd))

        if not cmd.endswith(self.command_terminator):
            c = cmd + self.command_terminator
        else:
            c = cmd
        return self.conn.write(c.encode(self.encoding))


    def write_raw(self, cmd):
        """
        Send "raw" data to device. Data is send as is withouth any transformations.
        """
        if self.verbose:
            print('%s: write_raw: %s' % (__name__, cmd))

        return self.conn.write(cmd)


    def read(self):
        """
        Read response string from device. Empty string is returned if
        device doesnt respond within the timeout set.

        Returned data is encoded to a string.
        """
        buf = self.conn.read()
        buf = buf.decode(self.encoding)

        if self.verbose:
            print('%s: read: %s' % (__name__, buf))

        return buf


    def read_raw(self):
        """
        Read raw response from device. This function returns bytes.
        """
        if self.verbose:
            print('%s: read_raw: %s' % (__name__, buf))

            return self.conn.read()


    def unit_ready(self, retries=3, delay=0.1):
        """
        Wait for unit to be ready by issuing *OPC? command and checking
        that returned value is "1".  If unit is not ready (returns "0"),
        then wait for :delay: seconds and attempt again upto :retries:
        times.

        command and query methods use this to wait for device to become
        ready before sending data to device.
        """
        count = 0

        if self.quirk_no_opc:
            time.sleep(self.no_opc_delay)
            return 1

        while (count < retries):
            self._opc()
            r = self.read()
            if (r == '1'):
                return 1
            count += 1
            time.sleep(delay)

        return 0


    def command(self, cmd):
        """
        Send a SCPI command to device after waiting device to become ready.
        If device is not ready SCPIError exception is raised.

        If command is missing terminator (default: \n) it is appended automatically.

        Return value: Response to SYST:ERR? after executing command.
        """
        if self.verbose:
            print('%s: send_command: %s' % (__name__, cmd))

        if not self.unit_ready():
            raise SCPIError("Device not ready!")

        self.write(cmd)

        if self.quirk_no_syst_err:
            return '0, "No Error"'

        return self._syst_err()


    def query(self, cmd):
        """
        Send a SCPI command to device and wait for response.
        Before sending command check and wait for device to be ready.
        If device is not ready SCPIError exception is raised.

        If command is missing terminator (default: \n) it is appended automatically.

        Return value: Response from unit to the command.
        """
        if self.verbose:
            print('%s: send_query: %s' % (__name__, cmd))

        if not self.unit_ready():
            raise SCPIError("Device not ready!")

        self.write(cmd)
        resp = self.read()

        if self.verbose:
            print("%s: response: '%s'" % (__name__, resp))

        self._syst_err()

        return resp


    # SCPI standard commands (possible of override by subclassing...)

    def _syst_err(self):
        self.write('SYST:ERR?')
        self.last_error = self.read()
        return self.last_error

    def _idn(self):
        return self.query('*IDN?')

    def _cls(self):
        return self.write('*CLS')

    def _opc(self):
        return self.write('*OPC?')


