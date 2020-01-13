# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-13 16:43:38

try:
    from ansible.module_utils.datamodel import DataModel
    from ansible.module_utils.stcrest import StcRest
    from ansible.module_utils.linker import Linker
except ImportError:
    from module_utils.datamodel import DataModel
    from module_utils.stcrest import StcRest
    from module_utils.linker import Linker

import requests
import pickle
import time
import json
import re


class Templater:
    def __init__(self, val):
        self.val = val

    def instance(self, index):
        return self._instance(self.val, index)

    def _instance(self, val, index):

        if type(val) is str:

            return self._evaluate(val, index)

        elif type(val) is list:

            xval = []
            for v in val:
                xval.append(self._instance(v, index))
            return xval

        elif type(val) is dict:

            xval = {}
            for i in val.keys():
                xval[i] = self._instance(val[i], index)
            return xval

        elif not val or type(val) is int or type(val) is bool:

            return val

        else:

            raise Exception("Templater - unknown type: %s" % (type(val)))

    def _evaluate(self, val, index):

        val = val.replace("$item", str(index + 1))
        val = val.replace("${item}", str(index + 1))
        val = val.replace("${item+1}", str(index + 2))
        return val
