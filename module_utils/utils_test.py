# -*- coding: utf-8 -*-

from module_utils.utils import *

class TestUtils:
    def test1a(self):
        names = "port[1:4] ethernet2/5 [4:9]_Ethernet1_9"
        retList = ['port1', 'port2', 'port3', 'port4', 'ethernet2/5', '4_Ethernet1_9', '5_Ethernet1_9', '6_Ethernet1_9', '7_Ethernet1_9', '8_Ethernet1_9', '9_Ethernet1_9']
        v = resolveNames(names)
        assert v == retList

    def test2a(self):
        ports = "//chassis[0]/1/1-3,6,8 //chassis[0]/5/7 //chassis[1]/2/1-3,6-8"
        retList = ['//chassis[0]/1/1', '//chassis[0]/1/2', '//chassis[0]/1/3', '//chassis[0]/1/6', '//chassis[0]/1/8', '//chassis[0]/5/7', '//chassis[1]/2/1', '//chassis[1]/2/2', '//chassis[1]/2/3', '//chassis[1]/2/6', '//chassis[1]/2/7', '//chassis[1]/2/8']
        v = resolvePorts(ports)
        assert v == retList
