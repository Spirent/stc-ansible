# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-02-06 12:21:19

try:
    from ansible.module_utils.datamodel import DataModel
    from ansible.module_utils.stcrest import StcRest
    from ansible.module_utils.xpath import Linker
except ImportError:
    from module_utils.datamodel import DataModel
    from module_utils.stcrest import StcRest
    from module_utils.xpath import Linker

import requests
import pickle
import time
import json
import math
import re


class Templater:

    def __init__(self, datamodel):
        self.datamodel = datamodel

    def get(self, val, index):

        if type(val) is str:

            return self._evaluate(val, index)

        elif type(val) is list:

            xval = []
            for v in val:
                xval.append(self.get(v, index))
            return xval

        elif type(val) is dict:

            xval = {}
            for i in val.keys():
                xval[i] = self.get(val[i], index)
            return xval

        elif not val or type(val) is int or type(val) is bool:

            return val

        else:

            raise Exception("Templater - unknown type: %s" % (type(val)))

    def _evaluate(self, value, index):

        value = value.replace("$item", str(index))

        matches = re.findall(r"(\${(.*?(\bnames\b).*?)})", value)
        for match in matches:
            key = match[0]
            val = eval(match[1], {"item": index, "math": math, "names": BoundedNamesArray(self.datamodel.names)})
            value = value.replace(key, str(val))

        #matches = re.findall(r"(\${(.*?((\bports\b)|(\bitem\b)).*?)})", value)
        matches = re.findall(r"(\${(.*?(\bports\b).*?)})", value)
        for match in matches:
            key = match[0]
            val = eval(match[1], {"item": index, "math": math, "ports": BoundedPortArray(self.datamodel.ports)})
            value = value.replace(key, str(val))

        matches = re.findall(r"(\${(.*?((\bchassis\b)|(\bitem\b)).*?)})", value)
        for match in matches:
            key = match[0]
            val = eval(match[1], {"item": index, "math": math, "chassis": BoundedChassisArray(self.datamodel.chassis)})
            value = value.replace(key, str(val))

        if value.find("${chassis-item}") >= 0:
            chassis = self.datamodel.getChassis(index)
            if chassis == None:
                print("Can not get chassis %d" % (index))
                chassis = "(Offline)"
            value = value.replace("${chassis-item}", chassis)

        return value


class BoundedChassisArray:

    def __init__(self, l):
        self.l = l

    def __getitem__(self, index):
        if index < len(self.l):
            return self.l[index]
        return "(no chassis [" + str(index) + "])"


class BoundedPortArray:

    def __init__(self, l):
        self.l = l

    def __getitem__(self, index):
        if index < len(self.l):
            return self.l[index]
        return "//(no port [" + str(index) + "])/1/1"


class BoundedNamesArray:

    def __init__(self, l):
        self.l = l

    def __getitem__(self, index):
        if index < len(self.l):
            return self.l[index]
        return "noPortName"

