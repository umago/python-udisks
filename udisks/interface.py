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

class Interface:

    def __init__(self, object_path):
        self.bus = dbus.SystemBus()
        self.object_path = object_path    
        self.object = self.bus.get_object("org.freedesktop.UDisks", self.object_path)
        self.properties_iface = dbus.Interface(self.object, dbus.PROPERTIES_IFACE)
    
    def _get_property(self, name): 
        return self.properties_iface.Get('org.freedesktop.UDisks.Device', name)

    def __str__(self):
        return str(self.object_path)
