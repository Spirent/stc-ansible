# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-15 15:11:56

from datetime import datetime
import logging


logging.basicConfig(
    filemode='w', 
    level=logging.INFO,
    filename='/tmp/stc-ansible.log', 
    format='%(name)s - %(levelname)s - %(message)s'
    )

class Logger:

    def __init__(self, module):
        self.module = module

    def error(self, msg):
        self.print(logging.ERROR, msg)

    def warning(self, msg):
        self.print(logging.WARNING, msg)

    def info(self, msg):
        self.print(logging.INFO, msg)

    def debug(self, msg):
        self.print(logging.DEBUG, msg)

    def print(self, severity, msg):
        msg = "%s [\033[93m%s\033[0m:\033[92m%-10s\033[0m] %s" % (datetime.now(), severity, self.module, msg)
        logging.info("%s %s %s"%(severity, self.module, msg))
        if severity>=logging.WARNING:
            print(msg)
