# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-14 10:44:02

from module_utils.datamodel import DataModel
from module_utils.linker import NodeSelector, Linker


class TestSelector:

    def createModel(self):
        self.dm = DataModel()
        self.dm.new("dummy-session")

        self.root = project1 = self.dm.insert("project1",
                                              {"object_type": "project"})

        dev1 = self.dm.insert("emulateddevice1", {
            "object_type": "emulateddevice",
            "name": "Device 1"
        }, project1)
        self.dm.insert("ipv4if1", {
            "object_type": "ipv4if",
            "name": "ipv4if 1"
        }, dev1)

        dev2 = self.dm.insert("emulateddevice2",
                              {"object_type": "emulateddevice"}, project1)
        self.dm.insert("ipv4if2", {
            "object_type": "ipv4if",
            "name": "ipv4if 2"
        }, dev2)

    def test1(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select("emulateddevice")
        assert n == 2

    def test2(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select("xproject")
        assert n == 0

    def test3(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select("emulateddevice", "name", "device 1")
        assert n == 1

    def test4(self):
        self.createModel()
        selector = NodeSelector(self.root)
        n = selector.select("emulateddevice", "name", "device x")
        assert n == 0

    def test5(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select("emulateddevice")
        n = selector.select("ipv4if")
        assert n == 2

    def test6(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select("emulateddevice", "name", "device 1")
        n = selector.select("ipv4if")
        assert n == 1

    def test7(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select("emulateddevice", "name", "device 1")
        n = selector.select("ipv4if", "name", "ipv4if 1")
        assert n == 1

    def test8(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select("emulateddevice")
        n = selector.select("ipv4if", "name", "ipv4if 1")
        assert n == 1

    def test9(self):
        self.createModel()
        selector = NodeSelector(self.root)
        selector.select("emulateddevice", "name", "device 2")
        n = selector.select("ipv4if", "name", "ipv4if 1")
        assert n == 0


class TestLinker:

    def createModel(self):
        self.dm = DataModel()
        self.dm.new("dummy-session")

        self.root = project1 = self.dm.insert("project1",
                                              {"object_type": "project"})

        self.port = port1 = self.dm.insert("port1", {
            "object_type": "port",
            "name": "port 1"
        }, project1)

        self.dev1 = self.dm.insert("emulateddevice1", {
            "object_type": "emulateddevice",
            "name": "Device 1"
        }, port1)
        self.ip1 = self.dm.insert("ipv4if1", {
            "object_type": "ipv4if",
            "name": "ipv4if 1"
        }, self.dev1)

        self.dev2 = self.dm.insert("emulateddevice2",
                                   {"object_type": "emulateddevice"}, port1)
        self.ip2 = self.dm.insert("ipv4if2", {
            "object_type": "ipv4if",
            "name": "ipv4if 2"
        }, self.dev2)

        return self.dm

    def test1(self):
        linker = Linker(self.createModel())
        node = linker.resolve("/port[name=port 1]")
        assert node == self.port

    def test2(self):
        linker = Linker(self.createModel())
        node = linker.resolve("/port[name=port 1]/emulateddevice")
        assert node == self.dev1

    def test2(self):
        linker = Linker(self.createModel())
        node = linker.resolve("/port[name=port 1]/emulateddevice[*]")
        assert node == self.dev1

    def test3(self):
        linker = Linker(self.createModel())
        node = linker.resolve("/port[name=port 1]/emulateddevice[*]/ipv4if")
        assert node == self.ip1
