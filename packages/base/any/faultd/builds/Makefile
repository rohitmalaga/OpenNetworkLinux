# -*- Makefile -*-
############################################################
# <bsn.cl fy=2013 v=onl>
#
#        Copyright 2013, 2014 Big Switch Networks, Inc.
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
# </bsn.cl>
############################################################
include $(ONL)/make/any.mk

MODULE := faultd-module
include $(BUILDER)/standardinit.mk

LIBRARY := faultd-main
$(LIBRARY)_SUBDIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(BUILDER)/lib.mk


DEPENDMODULES := faultd AIM

include $(BUILDER)/dependmodules.mk

BINARY := faultd.bin
$(BINARY)_LIBRARIES := $(LIBRARY_TARGETS)
include $(BUILDER)/bin.mk

include $(BUILDER)/targets.mk

GLOBAL_CFLAGS += -DAIM_CONFIG_INCLUDE_MODULES_INIT=1
GLOBAL_CFLAGS += -DAIM_CONFIG_INCLUDE_MAIN=1
GLOBAL_CFLAGS += -DAIM_CONFIG_INCLUDE_PVS_SYSLOG=1
GLOBAL_CFLAGS += -DAIM_CONFIG_INCLUDE_DAEMONIZE=1
GLOBAL_CFLAGS += -DFAULTD_CONFIG_INCLUDE_MAIN=1
GLOBAL_CFLAGS += -DFAULTD_CONFIG_INCLUDE_AIM_MAIN=1
GLOBAL_CFLAGS += -g

GLOBAL_LINK_LIBS += -lpthread

