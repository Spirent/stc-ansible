# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-16 23:15:15

from datetime import datetime
import logging


logging.basicConfig(
    filemode='w', 
    level=logging.INFO,
    filename='/tmp/stc-ansible.log', 
    format='%(name)s - %(levelname)s - %(message)s'
    )


class Logger:

    logLevel = logging.WARNING

    def __init__(self, module):
        self.module = module

    def error(self, msg):
        self.show(logging.ERROR, msg)

    def warning(self, msg):
        self.show(logging.WARNING, msg)

    def info(self, msg):
        self.show(logging.INFO, msg)

    def debug(self, msg):
        self.show(logging.DEBUG, msg)

    def setVerbose():
        Logger.logLevel = logging.DEBUG

    def show(self, severity, msg):
        msg = "%s [\033[93m%s\033[0m:\033[92m%-10s\033[0m] %s" % (datetime.now(), severity, self.module, msg)
        logging.info("%s %s %s"%(severity, self.module, msg))
        if severity>=Logger.logLevel:
            print(msg)
