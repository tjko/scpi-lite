#!/usr/bin/env python3
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

from setuptools import *

with open("README.md", "r") as fh:
    readme_text = fh.read()

setup(
    name="scpi-lite",
    version="0.2",
    license="GPL",
    author="Timo Kokkonen",
    author_email="tjko@iki.fi",
    url="https://github.com/tjko/scpi-lite/",
    description="Lightweight SCPI library for easy scripting access to instrument.",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    keywords=["scpi", "usbtmc"],
    platforms='any',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=['pyserial']
)

