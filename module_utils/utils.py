# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-19 22:23:54
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-19 23:43:41


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
