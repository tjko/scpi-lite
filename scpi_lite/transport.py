#
# transport.py
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

class SCPITransport:
    """
    A base class for implementing a transport for SCPIDevice class.
    """

    conn = None
    verbose = 0

    def __init__(self, device):
        """
        A transport implementation  must override this constructor.
        """

        raise NotImplementedError()

    def read(self):
        """
        Read data (reponse) from the device.
        """

        raise NotImplementedError()

    def write(self, data):
        """
        Send data (command) to the device.
        """

        raise NotImplementedError()

    def pending_input(self):
        """
        Return the number of bytes in the input buffer.
        """
        return 0

    def flush_input(self):
        """
        Flush input buffer, discarding all its contents.
        """

    def flush_output(self):
        """
        Flush output buffer, discarding all its contents.
        """

    def close(self):
        """
        Close connection.
        """


