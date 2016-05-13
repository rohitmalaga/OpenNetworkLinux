#!/usr/bin/python
################################################################
#
#        Copyright 2016, Big Switch Networks, Inc.
#
# Licensed under the Eclipse Public License, Version 1.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#        http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.
#
################################################################
#
# Wrapper object class for use with the onlp fan library.
#
################################################################
import ctypes
from ctypes.util import find_library
import os
import struct
from ctypes import byref
import pdb
import oid

#onlp_fan_caps
onlp_fan_caps =  {
    'ONLP_FAN_CAPS_B2F' : (1 << 0),
    'ONLP_FAN_CAPS_F2B' : (1 << 1),
    'ONLP_FAN_CAPS_SET_RPM' : (1 << 2),
    'ONLP_FAN_CAPS_SET_PERCENTAGE' : (1 << 3),
    'ONLP_FAN_CAPS_GET_RPM' : (1 << 4),
    'ONLP_FAN_CAPS_GET_PERCENTAGE' : (1 << 5),
}

#onlp_fan_dir
onlp_fan_dir =  {
    'ONLP_FAN_DIR_B2F' : 'B2F',
    'ONLP_FAN_DIR_F2B': 'F2B',
    'ONLP_FAN_DIR_LAST' : 'F2B',
    'ONLP_FAN_DIR_COUNT' : 0,
    'ONLP_FAN_DIR_INVALID' : -1,
}

#onlp_fan_mode 
onlp_fan_mode = {
    'ONLP_FAN_MODE_OFF': 'OFF',
    'ONLP_FAN_MODE_SLOW' : 'SLOW',
    'ONLP_FAN_MODE_NORMAL' : 'NORMAL',
    'ONLP_FAN_MODE_FAST' : 'FAST',
    'ONLP_FAN_MODE_MAX': 'MAX',
    'ONLP_FAN_MODE_LAST' : 'MAX',
    'ONLP_FAN_MODE_COUNT': 0,
    'ONLP_FAN_MODE_INVALID' : -1,
}

# onlp_fan_status
onlp_fan_status = {
    'ONLP_FAN_STATUS_PRESENT' : (1 << 0),
    'ONLP_FAN_STATUS_FAILED' : (1 << 1),
    'ONLP_FAN_STATUS_B2F' : (1 << 2),
    'ONLP_FAN_STATUS_F2B' : (1 << 3),
}

class ONLPFanException(Exception):
    pass


class onlp_fan_info(ctypes.Structure):
    _fields_ = [('onlp_oid_hdr_t',oid.onlp_oid_hdr),                    #OID Header
                ('status',ctypes.c_uint),                               #Status
                ('caps',ctypes.c_uint),                                 #Capabilities
                ('rpm',ctypes.c_int),                                   #Current fan speed, in RPM, if available
                ('percentage',ctypes.c_int),                            #Current fan percentage, if available
                ('model',ctypes.c_char*64),                             #Model (if applicable) 
                ('serial',ctypes.c_char*64),                            #Serial Number (if applicable)
                ('onlp_fan_mode',ctypes.c_char*16)]                     #Current fan mode, if available


class FAN(object):
    """" Light python wrapper around the ONLP Fan library """

# Loading libonlp library
    libonlp = 'libonlp.so.1'
    onlppath = os.path.join(*(os.path.split(__file__)[:-1] + (libonlp,)))
    onlp = ctypes.cdll.LoadLibrary(onlppath)
    
    def __init__(self):
        """  %brief This function is for initializing the fan subsystem.
        %param None
        %return 0 if successful
         """
        err = FAN.onlp.onlp_init()
        #err = FAN.onlp.onlp_fan_init()
        if err != 0: 
            raise ONLPFanException("Fan_init failed: " + str(err))

    def onlp_fan_info_get(self,oid,info):
        """  %brief This function is for getting FAN information
        %param oid: The FAN OID
        %param info: Receives the information structure.
        %return 0 if successful
        """
        rv = FAN.onlp.onlp_fan_info_get(oid,ctypes.byref(info))
        if rv < 0:
            raise ONLPFanDException("ONLP Fan get failed: " + str(rv))
        return rv

    def onlp_fan_rpm_set(self,oid,rpm):
        """ %brief: Set the fan speed in RPMs.
            Note: Only valid if the fan has the SET_RPM capability.
            %param oid : The Fan OID.
            %param rpm: The new RPM.
            %return less then 0 if error
        """
        return FAN.onlp.onlp_rpm_set(oid,rpm)

    def onlp_fan_percentage_set(self,oid,percentage):
        """ %brief: Set the fan speed in percentage.
            Note: Only valid if the fan has the SET_PERCENTAGE capability.
            %param oid : The FAN OID.
            %param  percentage: The percentage.
            %return less then 0 if error
        """
        return FAN.onlp.onlp_fan_percentage_set(oid,percentage)

    def onlp_fan_mode_set(self,oid,mode):
        """ %brief: Set the fan speed by mode.
            %param oid : The FAN OID.
            %param  mode: The fan mode value.
            %return less then 0 if error
        """
        return FAN.onlp.onlp_fan_mode_set(oid,mode)

    def onlp_fan_dir_set(self,oid,direction):
        """ %brief: Set the fan direction.
            Note: Only called if both capabilities are set.
            %param oid : The FAN OID.
            %param  mode: dir The fan direction (B2F or F2B).
            %return less then 0 if error
        """
        return FAN.onlp.onlp_fan_dir_set(oid,direction)

    def onlp_fan_dump(self,oid):
        """ %brief: FAN OID debug dump.
            %param oid : The Fan OID.
            %return None
        """
        # TODO Need to implement

    def onlp_fan_show(self,oid):
        """ %brief: Show the given FAN OID.
            %param oid : The Fan OID.
            %return None
        """
        # TODO Need to implement


if __name__ == '__main__': 
    fan_obj = FAN()
