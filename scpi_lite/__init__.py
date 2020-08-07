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

"""
scpi_lite is a lightweight SCPI library. It allows eaily sending SCPI commands
to various instruments over Serial, TCP, or USBTMC connection.

This library does not attempt to abstract instruments, but to only provide
simple yet robust means of sending SCPI commands/queries to instruments.

See https://github.com/tjko/scpi_lite/ for more information.
"""

__version__ = 0.2

VERSION = __version__

from .scpi import *
from .exceptions import *
