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

# onlp_led_caps 
onlp_led_caps = {
    'ONLP_LED_CAPS_ON_OFF' : (1 << 0),
    'ONLP_LED_CAPS_RED' : (1 << 10),
    'ONLP_LED_CAPS_RED_BLINKING' : (1 << 11),
    'ONLP_LED_CAPS_ORANGE' : (1 << 12),
    'ONLP_LED_CAPS_ORANGE_BLINKING' : (1 << 13),
    'ONLP_LED_CAPS_YELLOW' : ( 1 << 14),
    'ONLP_LED_CAPS_YELLOW_BLINKING' : (1 << 15),
    'ONLP_LED_CAPS_GREEN' : (1 << 16),
    'ONLP_LED_CAPS_GREEN_BLINKING' : (1 << 17),
    'ONLP_LED_CAPS_BLUE' : (1 << 18),
    'ONLP_LED_CAPS_BLUE_BLINKING' : (1 << 19),
    'ONLP_LED_CAPS_PURPLE' : (1 << 20),
    'ONLP_LED_CAPS_PURPLE_BLINKING' : (1 << 21),
    'ONLP_LED_CAPS_AUTO' :  (1 << 22),
}

# onlp_led_mode 
onlp_led_mode =  {
    'ONLP_LED_MODE_OFF':'OFF',
    'ONLP_LED_MODE_ON': 'ON',
    'ONLP_LED_MODE_BLINKING':'BLINKING',
    'ONLP_LED_MODE_RED' : 10,
    'ONLP_LED_MODE_RED_BLINKING' : 11,
    'ONLP_LED_MODE_ORANGE' : 12,
    'ONLP_LED_MODE_ORANGE_BLINKING' : 13,
    'ONLP_LED_MODE_YELLOW' : 14,
    'ONLP_LED_MODE_YELLOW_BLINKING' : 15,
    'ONLP_LED_MODE_GREEN' : 16,
    'ONLP_LED_MODE_GREEN_BLINKING' : 17,
    'ONLP_LED_MODE_BLUE' : 18,
    'ONLP_LED_MODE_BLUE_BLINKING' : 19,
    'ONLP_LED_MODE_PURPLE' : 20,
    'ONLP_LED_MODE_PURPLE_BLINKING' : 21,
    'ONLP_LED_MODE_AUTO': 22,
}

# onlp_led_status
onlp_led_status =  {
    'ONLP_LED_STATUS_PRESENT' : (1 << 0),
    'ONLP_LED_STATUS_FAILED' : (1 << 1),
    'ONLP_LED_STATUS_ON' : (1 << 2),
}

class ONLPLEDException(Exception):
    pass


class onlp_led_info(ctypes.Structure):
    _fields_ = [('onlp_oid_hdr_t',oid.onlp_oid_hdr),
                ('status',ctypes.c_uint),
                ('caps',ctypes.c_uint),
                ('onlp_led_mode',ctypes.c_int)]


class LED(object):
    """" Light python wrapper around the ONLP LED library """

# Loading libonlp library
    libonlp = 'libonlp.so.1'
    onlppath = os.path.join(*(os.path.split(__file__)[:-1] + (libonlp,)))
    onlp = ctypes.cdll.LoadLibrary(onlppath)
    
    def __init__(self):
        """  %brief This function is for initializing the led subsystem.
        %param None
        %return 0 if successful
         """
        err = LED.onlp.onlp_init()
        #err = LED.onlp.onlp_led_init()
        if err != 0: 
            raise ONLPLEDException("LED_init failed: " + str(err))

    def onlp_led_info_get(self,oid,info):
        """  %brief This function is for getting LED information
        %param oid: The LED OID
        %param info: Receives the information structure.
        %return 0 if successful
        """
        rv = LED.onlp.onlp_led_info_get(oid,ctypes.byref(info))
        if rv < 0:
            raise ONLPLEDException("ONLP LED get  failed: " + str(rv))
        return rv

    def onlp_led_set(self,oid,switch):
        """ %brief: Turn an LED on or off.
            Note: the purposes of this function the
            interpretation of "on" for multi-mode or multi-color LEDs
            is up to the platform implementation.
            %param oid : The LED OID.
            %param  swicth: on_or_off Led on (1) or LED off (0)
            %return 0 if successful
        """
        return LED.onlp.onlp_led_set(oid,switch) == 0

    def onlp_led_mode_set(self,oid,color):
        """ %brief: Set the LED color.
            Note: Only relevant if the LED supports the color capability.
            %param oid : The LED OID.
            %param  color: The color
            %return 0 if successful
        """
        err =  LED.onlp.onlp_led_mode_set(oid,color)
        if err < 0:
            raise ONLPLEDException("LED color change not possiable: " + str(err))
 
    def onlp_led_dump(self,oid):
        """ %brief: LED OID debug dump.
            %param oid : The LED OID.
            %return None
        """
        # Need to implement

    def onlp_led_show(self,oid):
        """ %brief: Show the given LED OID.
            %param oid : The LED OID.
            %return None
        """
        # Need to implement


if __name__ == '__main__': 
    led_obj = LED()
