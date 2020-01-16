# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-17 03:18:30

from module_utils.datamodel import DataModel
from module_utils.xpath import NodeSelector, Linker, Selector


class TestSelector:

    def createModel(self):
        self.dm = DataModel()
        self.dm.new("dummy-session", [])

        self.root = project1 = self.dm.insert("project1", {"object_type": "project"})

        dev1 = self.dm.insert("emulateddevice1", {"object_type": "emulateddevice", "name": "Device 1"}, project1)
        self.dm.insert("ipv4if1", {"object_type": "ipv4if", "name": "ipv4if 1"}, dev1)

        dev2 = self.dm.insert("emulateddevice2", {"object_type": "emulateddevice"}, project1)
        self.dm.insert("ipv4if2", {"object_type": "ipv4if", "name": "ipv4if 2"}, dev2)

    def test1(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select(Selector("emulateddevice"))
        assert n == 2

    def test2(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select(Selector("xproject"))
        assert n == 0

    def test3(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select(Selector("emulateddevice [ name = device 1]"))
        assert n == 1

    def test4(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select(Selector("emulateddevice [name= device x]"))
        assert n == 0

    def test5(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select(Selector("emulateddevice"))
        n = selector.select(Selector("ipv4if"))
        assert n == 2

    def test6(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select(Selector("emulateddevice [ name = device 1]"))
        n = selector.select(Selector("ipv4if"))
        assert n == 1

    def test7(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select(Selector("emulateddevice [ name = device 1]"))
        n = selector.select(Selector("ipv4if [ name = ipv4if 1 ]"))
        assert n == 1

    def test8(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select(Selector("emulateddevice"))
        n = selector.select(Selector("ipv4if [ name = ipv4if 1 ]"))
        assert n == 1

    def test9(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select(Selector("emulateddevice [ name = device 2]"))
        n = selector.select(Selector("ipv4if [ name = ipv4if 1 ]"))
        assert n == 0


class TestLinker:

    def createModel(self):
        self.dm = DataModel()
        self.dm.new("dummy-session", [])

        self.root = project1 = self.dm.insert("project1", {"object_type": "project"})

        self.port1 = port1 = self.dm.insert("port1", {"object_type": "port", "name": "port 1"}, project1)
        self.port2 = port2 = self.dm.insert("port2", {"object_type": "port", "name": "port 2"}, project1)

        self.dev1 = self.dm.insert("emulateddevice1", {"object_type": "emulateddevice", "name": "Device 1"}, port1)
        self.ip1 = self.dm.insert("ipv4if1", {"object_type": "ipv4if", "name": "ipv4if 1"}, self.dev1)

        self.dev2 = self.dm.insert("emulateddevice2", {"object_type": "emulateddevice", "name": "dev 2", "count":3}, port1)
        self.ip2 = self.dm.insert("ipv4if2", {"object_type": "ipv4if", "name": "ipv4if 2"}, self.dev2)

        self.dev3 = self.dm.insert("emulateddevice2", {"object_type": "emulateddevice", "name": "dev 3"}, port2)
        self.ip3 = self.dm.insert("ipv4if2", {"object_type": "ipv4if", "name": "ipv4if 3"}, self.dev3)

        return self.dm

    def test1(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name=port 1]")
        assert nodes.count() == 1 and nodes.get(0) == self.port1

    def test2(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name=port 1]/emulateddevice")
        assert nodes.count() == 2 and nodes.get(0) == self.dev1

    def test3a(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name=port 1]/emulateddevice")
        assert nodes.count() == 2 and nodes.get(0) == self.dev1 and nodes.get(1) == self.dev2

    def test3b(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name=port 1]/emulateddevice[*]")
        assert nodes.count() == 2 and nodes.get(0) == self.dev1 and nodes.get(1) == self.dev2

    def test4(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name=port 1]/emulateddevice[*]/ipv4if")
        assert nodes.count() == 2 and nodes.get(0) == self.ip1 and nodes.get(1) == self.ip2

    def test5(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name!= port 1]/emulateddevice/ipv4if")
        assert nodes.count() == 1 and nodes.get(0) == self.ip3

    def test7a(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name ~= Port]/emulateddevice/ipv4if")
        assert nodes.count() == 3

    def test7b(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name *= ort]/emulateddevice/ipv4if")
        assert nodes.count() == 3

    def test7c(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name ^= port]/emulateddevice/ipv4if")
        assert nodes.count() == 3

    def test7d(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[name ^= ort]/emulateddevice/ipv4if")
        assert nodes == None

    def test8a(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[0]/emulateddevice/ipv4if")
        assert nodes.count() == 2

    def test8b(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[1]/emulateddevice/ipv4if")
        assert nodes.count() == 1

    def test8c(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port[2]/emulateddevice/ipv4if")
        assert nodes == None

    def test9a(self):
        linker = Linker(self.createModel())
        nodes = linker._resolve("/port/emulateddevice[name *= dev][count = 3]/ipv4if")
        assert nodes.count() == 1
