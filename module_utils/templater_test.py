# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-20 12:51:37

from module_utils.templater import Templater
from module_utils.datamodel import DataModel
from module_utils.xpath import NodeSelector, Linker, Selector


class TestTemplater:

    def createTemplater(self, chassis=[]):
        dm = DataModel()
        dm.new("dummy-session", chassis)
        return Templater(dm)

    def test1(self):
        t = self.createTemplater(["abc"])
        v = t.get("${chassis[0]}", 0)
        assert v == 'abc'

    def test2(self):
        t = self.createTemplater()
        v = t.get("${chassis[0]}", 0)
        assert v == '(no chassis [0])'

    def test3(self):
        t = self.createTemplater()
        v = t.get("${item+1}", 1)
        assert v == 2
