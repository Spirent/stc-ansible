# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-19 22:23:54
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-19 23:43:41
import re

class Color:

    @staticmethod
    def blue(s):
        return "\033[94m" + s + "\033[0m"

    @staticmethod
    def green(s):
        return "\033[92m" + s + "\033[0m"

    @staticmethod
    def red(s):
        return "\033[91m" + s + "\033[0m"

    @staticmethod
    def bold(s):
        return "\033[97m" + s + "\033[0m"


class Result:

    def __init__(self):
        self.val = None
        self.err = None

    @staticmethod
    def error(err):

        r = Result()
        r.err = err
        return r

    @staticmethod
    def value(val):

        r = Result()
        r.val = val
        return r

    def isError(self):
        return self.err != None

    def __str__(self):
        if self.err:
            return "Error: " + str(self.err)
        if self.val:
            return "Value: " + str(self.val)
        return "No result"


def resolvePorts(ports):
    outList = []
    ports = ports.split(" ")
    for it in ports:
        tmList = it.rsplit('/', 1)
        # Handle exception
        if 2 != len(tmList):
            log.error("GET Invalid ports: %s" % (it))
            return outList

        key = tmList[0]
        port = tmList[1]

        # Handle ',' in ports
        portList = port.split(',') if ',' in port else [port]
        newList = []
        for each in portList:
            if '-' in each:
                start = int(each.split('-')[0])
                end = int(each.split('-')[1]) + 1
                newList += [key + '/' + str(item) for item in list(range(start, end))]
            else:
                newList.append(key + '/' + each)
        outList += newList

    return outList

def resolveNames(names):
    outList = []
    names = names.split(" ")
    for it in names:
        m = re.search(r'\[\d+:\d+\]', it)
        if m:
            rg = m.group()
            rgn = rg[1:len(rg) - 1].split(':')
            start = int(rgn[0])
            end = int(rgn[1]) + 1
            outList += [it.replace(rg, str(item)) for item in list(range(start, end))]
        else:
            outList += [it]

    return outList
    
