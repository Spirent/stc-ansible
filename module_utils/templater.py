# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-17 02:28:32

try:
    from ansible.module_utils.datamodel import DataModel
    from ansible.module_utils.stcrest import StcRest
    from ansible.module_utils.linker import Linker
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

        matches = re.findall(r"\${(.*?item.*?)}", value)
        for match in matches:
            key = "${" + match + "}"
            val = eval(match, {"item": index, "math": math})
            # print(index,">>>",key,val)
            value = value.replace(key, str(val))

        if value.find("${chassis-item}") >= 0:
            chassis = self.datamodel.getChassis(index)
            if chassis == None:
                print("Can not get chassis %d" % (index))
                chassis = "(Offline)"
            value = value.replace("${chassis-item}", chassis)

        elif value.find("${chassis-") >= 0:

            match = re.findall(r"\${chassis-([0-9]*)}", value)
            if len(match) > 0:
                index = match[0]
                chassis = self.datamodel.getChassis(int(index) - 1)
                if chassis == None:
                    print("Can not get chassis %s" % (index))
                    chassis = "(Offline)"
                value = value.replace("${chassis-" + index + "}", chassis)

        # print(value)
        return value
