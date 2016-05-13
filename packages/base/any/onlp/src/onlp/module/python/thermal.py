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
# Wrapper object class for use with the onlp thermal library.
#
################################################################
import ctypes
from ctypes.util import find_library
import os
import struct
from ctypes import byref
import pdb
import oid

# onlp_thermal_caps 
onlp_thermal_caps = {
    'ONLP_THERMAL_CAPS_GET_TEMPERATURE' : (1 << 0),
    'ONLP_THERMAL_CAPS_GET_WARNING_THRESHOLD' : (1 << 1),
    'ONLP_THERMAL_CAPS_GET_ERROR_THRESHOLD' : (1 << 2),
    'ONLP_THERMAL_CAPS_GET_SHUTDOWN_THRESHOLD' : (1 << 3),
}

# onlp_thermal_status
onlp_thermal_status = {
    'ONLP_THERMAL_STATUS_PRESENT' : (1 << 0),
    'ONLP_THERMAL_STATUS_FAILED' : (1 << 1),
}

# onlp_thermal_threshold
onlp_thermal_threshold = {
    'ONLP_THERMAL_THRESHOLD_WARNING_DEFAULT' : 45000,
    'ONLP_THERMAL_THRESHOLD_ERROR_DEFAULT' : 55000,
    'ONLP_THERMAL_THRESHOLD_SHUTDOWN_DEFAULT' : 60000,
}


class ONLPThermalException(Exception):
    pass

class thermal_thresholds(ctypes.Structure):
    _fields_ = [('warning',ctypes.c_int),
                ('error',ctypes.c_int),
                ('shutdown',ctypes.c_int)]

class onlp_thermal_info(ctypes.Structure):
    _fields_ = [('onlp_oid_hdr_t',oid.onlp_oid_hdr),
                ('status',ctypes.c_uint),
                ('caps',ctypes.c_uint),
                ('mcelsius',ctypes.c_int),
                ('temp_strut',thermal_thresholds)]


class THERMAL(object):
    """" Light python wrapper around the ONLP Thermal library """

# Loading libonlp library
    libonlp = 'libonlp.so.1'
    onlppath = os.path.join(*(os.path.split(__file__)[:-1] + (libonlp,)))
    onlp = ctypes.cdll.LoadLibrary(onlppath)
    
    def __init__(self):
        """  %brief This function is for initializing the thermal subsystem.
        %param None
        %return 0 if successful
         """
        err = THERMAL.onlp.onlp_init()
        #err = THERMAL.onlp.onlp_thermal_init()
        if err != 0: 
            raise ONLPThermalException("Thermal_init failed: " + str(err))

    def onlp_thermal_info_get(self,oid,info):
        """  %brief This function is for initializing the thermal subsystem.
        %param None
        %return 0 if successful
        """ 
        rv = THERMAL.onlp.onlp_thermal_info_get(oid,ctypes.byref(info))
        if rv < 0:
            raise ONLPThermalException("ONLP Thermal get  failed: " + str(rv))
        return rv
    
    def onlp_thermal_ioctl(self,code):
        """  %brief Thermal driver ioctl.
        %param code: Thermal ioctl code.
        %return 0 if successful
        """
        return THERMAL.onlp.onlp_thermal_ioctl(code)
    
    def onlp_thermal_vioctl(self,code,varg):
        """  %brief Thermal driver ioctl.
        %param code: Thermal ioctl code.
        %param vargs: vargs The arguments.
        %return 0 if successful
        """
        return THERMAL.onlp.onlp_thermal_vioctl(codei,varg)

    def onlp_thermal_dump(self,oid):
        """  %brief Thermal OID debug dump.
        %param OID: The thermal OID.
        %return none
        """
        info = onlp_thermal_info()
        rv = thermal_obj.onlp_thermal_info_get(oid,info)
        print rv
        

    def onlp_thermal_show(self,oid):
        """  %brief Show the given thermal OID.
        %param OID: The thermal OID.
        %return none
        """
       # TODO Need to implement
 

if __name__ == '__main__': 
    thermal_obj = THERMAL()
    #thermal_obj.onlp_thermal_dump(2)
