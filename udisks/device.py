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
from interface import DEVICE_IFACE
from exceptions import *

class Device(Interface):

    def __init__(self, object_path):
        Interface.__init__(self, object_path)
        self.dev_iface = dbus.Interface(self.object, DEVICE_IFACE)

    def _exec_func(self, func, args=()):
        try:
            return func(*args)
        except dbus.exceptions.DBusException, e:
            e_name = e.get_dbus_name()
            if e_name == "org.freedesktop.PolicyKit.Error.NotAuthorized":
                raise NotAuthorized(str(e))
            elif e_name == "org.freedesktop.UDisks.Error.Busy":
                raise Busy(str(e))
            elif e_name == "org.freedesktop.UDisks.Error.Failed":
                raise Failed(str(e))
            elif e_name == "org.freedesktop.UDisks.Error.Cancelled":
                raise Cancelled(str(e))
            elif e_name == "org.freedesktop.UDisks.Error.InvalidOption":
                raise InvalidOption(str(e))
            elif e_name == "org.freedesktop.UDisks.Error.FilesystemDriverMissing":
                raise FilesystemDriverMissing(str(e))
            elif e_name == "org.freedesktop.UDisks.Error.FilesystemToolsMissing":
                raise FilesystemToolsMissing(str(e))

    def JobCancel(self):
        self._exec_func(self.dev_iface.JobCancel)

    def PartitionTableCreate(self, scheme, options=''):
        self._exec_func(self.dev_iface.PartitionTableCreate, (scheme, options))

    def PartitionDelete(self, options=''):
        self._exec_func(self.dev_iface.PartitionDelete, (options,))

    def PartitionCreate(self, offset, size, type, label, flags,
                        options, fstype, fsoptions):
        dev = self._exec_func(self.dev_iface.PartitionCreate, (offset, size,
                                                               type, label,
                                                               flags, options,
                                                               fstype, fsoptions))
        return Device(dev)

    def PartitionModify(self, type, label, flags):
        self._exec_func(self.dev_iface.PartitionModify, (type, label, flags))

    def FilesystemCreate(self, fstype, options=''):
        self._exec_func(self.dev_iface.FilesystemCreate, (fstype, options))

    def FilesystemSetLabel(self, new_label):
        self._exec_func(self.dev_iface.FilesystemSetLabel, (new_label,))

    def FilesystemMount(self, filesystem_type, options=''):
        return self._exec_func(self.dev_iface.FilesystemMount, (filesystem_type, options))

    def FilesystemUnmount(self, options=''):
        self._exec_func(self.dev_iface.FilesystemUnmount, (options,))

    def FilesystemCheck(self, options=''):
        return bool(self._exec_func(self.dev_iface.FilesystemCheck, (options,)))

    def FilesystemListOpenFiles(self):
        l = list()
        files = self._exec_func(self.dev_iface.FilesystemListOpenFiles)
        for f in files:
            l.append((int(f[0]), int(f[1]), str(f[2])))
        return l

    def LuksUnlock(self, passphrase, options=''):
        raise NotImplementedError

    def LuksLock(self, options=''):
        raise NotImplementedError

    def LuksChangePassphrase(self, current_passphrase,  new_passphrase):
        raise NotImplementedError

    def LinuxMdAddComponent(self, component, options=''):
        raise NotImplementedError

    def LinuxMdRemoveComponent(self, component, options=''):
        raise NotImplementedError

    def LinuxMdStop(self, options=''):
        raise NotImplementedError 

    def LinuxLvm2LVStop(self, options=''):
        raise NotImplementedError

    def LinuxMdCheck(self, options=''):
        raise NotImplementedError

    def DriveInhibitPolling(self, options=''):
        raise NotImplementedError

    def DriveUninhibitPolling(self, cookie):
        raise NotImplementedError

    def DrivePollMedia(self):
        raise NotImplementedError

    def DriveEject(self, options=''):
        raise NotImplementedError

    def DriveDetach(self, options=''):
        raise NotImplementedError

    def DriveSetSpindownTimeout(self, timeout_seconds, options=''):
        raise NotImplementedError

    def DriveUnsetSpindownTimeout(self, cookie):
        raise NotImplementedError

    def DriveAtaSmartRefreshData(self, options=''):
        raise NotImplementedError

    def DriveAtaSmartInitiateSelftest(self, test, options=''):
        raise NotImplementedError

    def DriveBenchmark(self, do_write_benchmark, options=''):
        raise NotImplementedError

    @property
    def NativePath(self):
        return str(self._get_property('NativePath'))

    @property
    def DeviceDetectionTime(self):
        return int(self._get_property("DeviceDetectionTime"))

    @property
    def DeviceMediaDetectionTime(self):
        return int(self._get_property("DeviceMediaDetectionTime"))

    @property
    def DeviceMajor(self):
        return hex(self._get_property("DeviceMajor"))

    @property
    def DeviceMinor(self):
        return hex(self._get_property("DeviceMinor"))

    @property
    def DeviceFile(self):
        return str(self._get_property("DeviceFile"))

    @property
    def DeviceFilePresentation(self):
        return str(self._get_property("DeviceFilePresentation"))

    @property
    def DeviceFileById(self):
        l = list()
        for id in self._get_property("DeviceFileById"):
            l.append(str(id))
        return l

    @property
    def DeviceFileByPath(self):
        l = list()
        for id in self._get_property("DeviceFileByPath"):
            l.append(str(id))
        return l

    @property
    def DeviceIsSystemInternal(self):
        return bool(self._get_property("DeviceIsSystemInternal"))

    @property
    def DeviceIsPartition(self):
        return bool(self._get_property("DeviceIsPartition"))

    @property
    def DeviceIsPartitionTable(self):
        return bool(self._get_property("DeviceIsPartitionTable"))

    @property
    def DeviceIsRemovable(self):
        return bool(self._get_property("DeviceIsRemovable"))

    @property
    def DeviceIsMediaAvailable(self):
        return bool(self._get_property("DeviceIsMediaAvailable"))

    @property
    def DeviceIsMediaChangeDetected(self):
        return bool(self._get_property("DeviceIsMediaChangeDetected"))

    @property
    def DeviceIsMediaChangeDetectionPolling(self):
        return bool(self._get_property("DeviceIsMediaChangeDetectionPolling"))

    @property
    def DeviceIsMediaChangeDetectionInhibitable(self):
        return bool(self._get_property("DeviceIsMediaChangeDetectionInhibitable"))

    @property
    def DeviceIsMediaChangeDetectionInhibited(self):
        return bool(self._get_property("DeviceIsMediaChangeDetectionInhibited"))

    @property
    def DeviceIsReadOnly(self):
        return bool(self._get_property("DeviceIsReadOnly"))

    @property
    def DeviceIsDrive(self):
        return bool(self._get_property("DeviceIsDrive"))

    @property
    def DeviceIsOpticalDisc(self):
        return bool(self._get_property("DeviceIsOpticalDisc"))

    @property
    def DeviceIsMounted(self):
        return bool(self._get_property("DeviceIsMounted"))

    @property
    def DeviceMountPaths(self):
        l = list()
        for id in self._get_property("DeviceMountPaths"):
            l.append(str(id))
        return l

    @property
    def DeviceMountedByUid(self):
        return int(self._get_property("DeviceMountedByUid"))

    @property
    def DeviceIsLuks(self):
        return bool(self._get_property("DeviceIsLuks"))

    @property
    def DeviceIsLuksCleartext(self):
        return bool(self._get_property("DeviceIsLuksCleartext"))

    @property
    def DeviceIsLinuxMdComponent(self):
        return bool(self._get_property("DeviceIsLinuxMdComponent"))

    @property
    def DeviceIsLinuxMd(self):
        return bool(self._get_property("DeviceIsLinuxMd"))

    @property
    def DeviceIsLinuxLvm2LV(self):
        return bool(self._get_property("DeviceIsLinuxLvm2LV"))

    @property
    def DeviceIsLinuxLvm2PV(self):
        return bool(self._get_property("DeviceIsLinuxLvm2PV"))

    @property
    def DeviceIsLinuxDmmpComponent(self):
        return bool(self._get_property("DeviceIsLinuxDmmpComponent"))

    @property
    def DeviceIsLinuxDmmp(self):
        return bool(self._get_property("DeviceIsLinuxDmmp"))

    @property
    def DeviceSize(self):
        return long(self._get_property("DeviceSize"))

    @property
    def DeviceBlockSize(self):
        return int(self._get_property("DeviceBlockSize"))

    @property
    def DevicePresentationHide(self):
        return bool(self._get_property("DevicePresentationHide"))

    @property
    def DevicePresentationNopolicy(self):
        return bool(self._get_property("DevicePresentationNopolicy"))

    @property
    def DevicePresentationName(self):
        return str(self._get_property("DevicePresentationName"))

    @property
    def DevicePresentationIconName(self):
        return bool(self._get_property("DevicePresentationIconName"))

    @property
    def JobInProgress(self):
        return bool(self._get_property("JobInProgress"))

    @property
    def JobId(self):
        return str(self._get_property("JobId"))

    @property
    def JobInitiatedByUid(self):
        return int(self._get_property("JobInitiatedByUid"))

    @property
    def JobIsCancellable(self):
        return bool(self._get_property("JobIsCancellable"))

    @property
    def JobPercentage(self):
        return int(self._get_property("JobPercentage"))

    @property
    def IdUsage(self):
        return str(self._get_property("IdUsage"))

    @property
    def IdType(self):
        return str(self._get_property("IdType"))

    @property
    def IdVersion(self):
        return str(self._get_property("IdVersion"))

    @property
    def IdUuid(self):
        return str(self._get_property("IdUuid"))

    @property
    def IdLabel(self):
        return str(self._get_property("IdLabel"))

    @property
    def LuksHolder(self):
        raise NotImplementedError

    @property
    def LuksCleartextSlave(self):
        raise NotImplementedError

    @property
    def LuksCleartextUnlockedByUid(self):
        raise NotImplementedError

    @property
    def PartitionSlave(self):
        raise NotImplementedError

    @property
    def PartitionScheme(self):
        return str(self._get_property("PartitionScheme"))

    @property
    def PartitionType(self):
        return str(self._get_property("PartitionType"))

    @property
    def PartitionLabel(self):
        return str(self._get_property("PartitionLabel"))

    @property
    def PartitionUuid(self):
        return str(self._get_property("PartitionUuid"))

    @property
    def PartitionFlags(self):
        l = list()
        for id in self._get_property("PartitionFlags"):
            l.append(str(id))
        return l

    @property
    def PartitionNumber(self):
        return int(self._get_property("PartitionNumber"))

    @property
    def PartitionOffset(self):
        return long(self._get_property("PartitionOffset"))

    @property
    def PartitionSize(self):
        return long(self._get_property("PartitionSize"))

    @property
    def PartitionTableScheme(self):
        return str(self._get_property("PartitionTableScheme"))

    @property
    def PartitionTableCount(self):
        return int(self._get_property("PartitionTableCount"))

    @property
    def DriveVendor(self):
        return str(self._get_property("DriveVendor"))

    @property
    def DriveModel(self):
        return str(self._get_property("DriveModel"))

    @property
    def DriveRevision(self):
        return str(self._get_property("DriveRevision"))

    @property
    def DriveSerial(self):
        return str(self._get_property("DriveSerial"))

    @property
    def DriveWwn(self):
        return str(self._get_property("DriveWwn"))

    @property
    def DriveRotationRate(self):
        return int(self._get_property("DriveRotationRate"))

    @property
    def DriveWriteCache(self):
        return str(self._get_property("DriveWriteCache"))

    @property
    def DriveConnectionInterface(self):
        return str(self._get_property("DriveConnectionInterface"))

    @property
    def DriveConnectionSpeed(self):
        return long(self._get_property("DriveConnectionSpeed"))

    @property
    def DriveMediaCompatibility(self):
        l = list()
        for id in self._get_property("DriveMediaCompatibility"):
            l.append(str(id))
        return l

    @property
    def DriveMedia(self):
        return str(self._get_property("DriveMedia"))

    @property
    def DriveIsMediaEjectable(self):
        return bool(self._get_property("DriveIsMediaEjectable"))

    @property
    def DriveCanDetach(self):
        return bool(self._get_property("DriveCanDetach"))

    @property
    def DriveCanSpindown(self):
        return bool(self._get_property("DriveCanSpindown"))

    @property
    def DriveIsRotational(self):
        return bool(self._get_property("DriveIsRotational"))

    @property
    def DriveAdapter(self):
        raise NotImplementedError

    @property
    def DrivePorts(self):
        raise NotImplementedError

    @property
    def DriveSimilarDevices(self):
        raise NotImplementedError

    @property
    def OpticalDiscIsBlank(self):
        return bool(self._get_property("OpticalDiscIsBlank"))

    @property
    def OpticalDiscIsAppendable(self):
        return bool(self._get_property("OpticalDiscIsAppendable"))

    @property
    def OpticalDiscIsClosed(self):
        return bool(self._get_property("OpticalDiscIsClosed"))

    @property
    def OpticalDiscNumTracks(self):
        return int(self._get_property("OpticalDiscNumTracks"))

    @property
    def OpticalDiscNumAudioTracks(self):
        return int(self._get_property("OpticalDiscNumAudioTracks"))

    @property
    def OpticalDiscNumSessions(self):
        return int(self._get_property("OpticalDiscNumSessions"))

    @property
    def DriveAtaSmartIsAvailable(self):
        return bool(self._get_property("DriveAtaSmartIsAvailable"))

    @property
    def DriveAtaSmartTimeCollected(self):
        return long(self._get_property("DriveAtaSmartTimeCollected"))

    @property
    def DriveAtaSmartStatus(self):
        return str(self._get_property("DriveAtaSmartStatus"))

    @property
    def DriveAtaSmartBlob(self):
        raise NotImplementedError

    @property
    def LinuxMdComponentLevel(self):
        return str(self._get_property("LinuxMdComponentLevel"))

    @property
    def LinuxMdComponentPosition(self):
        return int(self._get_property("LinuxMdComponentPosition"))

    @property
    def LinuxMdComponentNumRaidDevices(self):
        return int(self._get_property("LinuxMdComponentNumRaidDevices"))

    @property
    def LinuxMdComponentUuid(self):
        return str(self._get_property("LinuxMdComponentUuid"))

    @property
    def LinuxMdComponentName(self):
        return str(self._get_property("LinuxMdComponentName"))

    @property
    def LinuxMdComponentHomeHost(self):
        return str(self._get_property("LinuxMdComponentHomeHost"))

    @property
    def LinuxMdComponentVersion(self):
        return str(self._get_property("LinuxMdComponentVersion"))

    @property
    def LinuxMdComponentHolder(self):
        raise NotImplementedError

    @property
    def LinuxMdComponentState(self):
        l = list()
        for id in self._get_property("LinuxMdComponentState"):
            l.append(str(id))
        return l

    @property
    def LinuxMdState(self):
        return str(self._get_property("LinuxMdState"))

    @property
    def LinuxMdLevel(self):
        return str(self._get_property("LinuxMdLevel"))

    @property
    def LinuxMdUuid(self):
        return str(self._get_property("LinuxMdUuid"))

    @property
    def LinuxMdHomeHost(self):
        return str(self._get_property("LinuxMdHomeHost"))

    @property
    def LinuxMdName(self):
        return str(self._get_property("LinuxMdName"))

    @property
    def LinuxMdNumRaidDevices(self):
        return int(self._get_property("LinuxMdNumRaidDevices"))

    @property
    def LinuxMdVersion(self):
        return str(self._get_property("LinuxMdVersion"))

    @property
    def LinuxMdSlaves(self):
        raise NotImplementedError

    @property
    def LinuxMdIsDegraded(self):
        return bool(self._get_property("LinuxMdIsDegraded"))

    @property
    def LinuxMdSyncAction(self):
        return str(self._get_property("LinuxMdSyncAction"))

    @property
    def LinuxMdSyncPercentage(self):
        return int(self._get_property("LinuxMdSyncPercentage"))

    @property
    def LinuxMdSyncSpeed(self):
        return long(self._get_property("LinuxMdSyncSpeed"))

    @property
    def LinuxLvm2PVUuid(self):
        return str(self._get_property("LinuxLvm2PVUuid"))

    @property
    def LinuxLvm2PVNumMetadataAreas(self):
        return int(self._get_property("LinuxLvm2PVNumMetadataAreas"))

    @property
    def LinuxLvm2PVGroupName(self):
        return str(self._get_property("LinuxLvm2PVGroupName"))

    @property
    def LinuxLvm2PVGroupUuid(self):
        return str(self._get_property("LinuxLvm2PVGroupUuid"))

    @property
    def LinuxLvm2PVGroupSize(self):
        return long(self._get_property("LinuxLvm2PVGroupSize"))

    @property
    def LinuxLvm2PVGroupUnallocatedSize(self):
        return long(self._get_property("LinuxLvm2PVGroupUnallocatedSize"))

    @property
    def LinuxLvm2PVGroupSequenceNumber(self):
        return long(self._get_property("LinuxLvm2PVGroupSequenceNumber"))

    @property
    def LinuxLvm2PVGroupExtentSize(self):
        return long(self._get_property("LinuxLvm2PVGroupExtentSize"))

    @property
    def LinuxLvm2PVGroupPhysicalVolumes(self):
        l = list()
        for id in self._get_property("LinuxLvm2PVGroupPhysicalVolumes"):
            l.append(str(id))
        return l

    @property
    def LinuxLvm2PVGroupLogicalVolumes(self):
        l = list()
        for id in self._get_property("LinuxLvm2PVGroupLogicalVolumes"):
            l.append(str(id))
        return l

    @property
    def LinuxLvm2LVName(self):
        return str(self._get_property("LinuxLvm2LVName"))

    @property
    def LinuxLvm2LVUuid(self):
        return str(self._get_property("LinuxLvm2LVUuid"))

    @property
    def LinuxLvm2LVGroupName(self):
        return str(self._get_property("LinuxLvm2LVGroupName"))

    @property
    def LinuxLvm2LVGroupUuid(self):
        return str(self._get_property("LinuxLvm2LVGroupUuid"))

    @property
    def LinuxDmmpComponentHolder(self):
        raise NotImplementedError

    @property
    def LinuxDmmpName(self):
        return str(self._get_property("LinuxDmmpName"))

    @property
    def LinuxDmmpSlaves(self):
        raise NotImplementedError

    @property
    def LinuxDmmpParameters(self):
        return str(self._get_property("LinuxDmmpParameters"))

