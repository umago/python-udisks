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

from device import Device
from adapter import Adapter
from expander import Expander
from port import Port

class UDisks:

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.proxy = self.bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
        self.iface = dbus.Interface(self.proxy, "org.freedesktop.UDisks")

    def EnumerateAdapters(self):
        """Enumerate all storage adapters on the system
        
        returns:
            An array of object paths for storage adapters
        """
        l = list()
        for i in self.iface.EnumerateAdapters():
            obj = Adapter(i)
            l.append(obj)
        return l

    def EnumerateExpanders(self):
        """Enumerate all storage expanders on the system

        returns:
            An array of object paths for storage expanders
        """
        l = list()
        for i in self.iface.EnumerateExpanders():
            obj = Expander(i)
            l.append(obj)
        return l

    def EnumeratePorts(self):
        """Enumerate all storage ports on the system

        returns:
            An array of object paths for ports
        """
        l = list()
        for i in self.iface.EnumeratePorts():
            obj = Port(i)
            l.append(obj)
        return l

    def EnumerateDevices(self):
        """Enumerate all disk devices on the system

        returns:
            An array of object paths for devices
        """
        l = list()
        for i in self.iface.EnumerateDevices():
            obj = Device(i)
            l.append(obj)
        return l

    def EnumerateDeviceFiles(self):
        """Enumerate all device files (including symlinks) for disk devices on the system.

        returns:
            An array device file names
        """
        l = list()
        for i in self.iface.EnumerateDeviceFiles():
            l.append(str(i))
        return l

    def FindDeviceByDeviceFile(self, device_file):
        """Finds a device by device path

        @device_file = UNIX special device file

        returns:
            Object path of device
        """
        return str(self.iface.FindDeviceByDeviceFile(device_file))

    def FindDeviceByMajorMinor(self, device_major, device_minor):
        #out 'o'  device
        return str(self.iface.FindDeviceByMajorMinor(device_major, device_minor))

    def DriveInhibitAllPolling(self, options):
        #out 's'  cookie
        pass

    def DriveUninhibitAllPolling(self, cookie):
        pass

    def DriveSetAllSpindownTimeouts(self, timeout_seconds, options):
        #out 's'  cookie
        pass

    def DriveUnsetAllSpindownTimeouts(self, cookie):
        pass

    def LinuxLvm2VGStart(self, uuid, options):
        pass

    def LinuxLvm2VGStop(self, uuid, options):
        pass

    def LinuxLvm2VGSetName(self, uuid, name):
        pass

    def LinuxLvm2VGAddPV(self, uuid, physical_volume, options):
        pass

    def LinuxLvm2VGRemovePV(self, vg_uuid, pv_uuid, options):
        pass

    def LinuxLvm2LVSetName(self, group_uuid, uuid, name):
        pass

    def LinuxLvm2LVStart(self, group_uuid, uuid, options):
        pass

    def LinuxLvm2LVRemove(self, group_uuid, uuid, options):
        pass

    def LinuxLvm2LVCreate(self, group_uuid, name,
                                size, num_stripes,
                                stripe_size, num_mirrors,
                                options, fstype, fsoptions):
        #out 'o'  created_device
        pass

    def LinuxMdStart(self, components, options):
        #out 'o'  device
        pass

    def LinuxMdCreate(self, components, level,
                            stripe_size, name, options):
        #out 'o'  device
        pass

    def Inhibit(self):
        #out 's'  cookie
        pass

    def Uninhibit(self, cookie):
        pass

    @property
    def DaemonVersion(self):
        return self.proxy.Get('org.freedesktop.UDisks', 'DaemonVersion')

    @property
    def DaemonIsInhibited(self):
        if self.proxy.Get('org.freedesktop.UDisks', 'DaemonIsInhibited'):
            return True
        return False

    @property
    def SupportsLuksDevices(self):
        if self.proxy.Get('org.freedesktop.UDisks', 'SupportsLuksDevices'):
            return True
        return False

    @property
    def KnownFilesystems(self):
        d = dict()
        for fs_info in self.proxy.Get('', 'KnownFilesystems'):
            d[str(fs_info[0])] = dict()
            d[fs_info[0]].update({"name": str(fs_info[1]),
                                  "supports_unix_owners": bool(fs_info[2]),
                                  "can_mount": bool(fs_info[3]),
                                  "can_create": bool(fs_info[4]),
                                  "max_label_len": int(fs_info[5]),
                                  "supports_label_rename": bool(fs_info[6]),
                                  "supports_online_label_rename": bool(fs_info[7]),
                                  "supports_fsck": bool(fs_info[8]),
                                  "supports_online_fsck": bool(fs_info[9]),
                                  "supports_resize_enlarge": bool(fs_info[10]),
                                  "supports_online_resize_enlarge": bool(fs_info[11]),
                                  "supports_resize_shrink": bool(fs_info[12]),
                                  "supports_online_resize_shrink": bool(fs_info[13])})
        return d

