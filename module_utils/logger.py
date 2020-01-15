# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-15 14:54:03

from datetime import datetime
import logging


class Logger:

    def __init__(self, module):
        self.module = module

    def error(self, msg):
        self.print("ERRO", msg)

    def warning(self, msg):
        self.print("WARN", msg)

    def info(self, msg):
        self.print("INFO", msg)

    def debug(self, msg):
        self.print("DEBG", msg)

    def print(self, severity, msg):
        print("%s [\033[93m%s\033[0m:\033[92m%-10s\033[0m] %s" % (datetime.now(), severity, self.module, msg))
