#!/usr/bin/python
# coding: utf-8
# Copyright (C) 2011 Lucas Alvares Gomes <lucasagomes@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import dbus

from interface import Interface

class Adapter(Interface):

    @property
    def NativePath(self):
        return str(self._get_property("NativePath"))

    @property
    def Vendor(self):
        return str(self._get_property("Vendor"))

    @property
    def Model(self):
        return str(self._get_property("Model"))

    @property
    def Driver(self):
        return str(self._get_property("Driver"))

    @property
    def NumPorts(self):
        return int(self._get_property("NumPorts"))

    @property
    def Fabric(self):
        return str(self._get_property("Fabric"))

