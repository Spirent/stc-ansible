# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-13 12:39:40

import requests
import pickle
import json
import re
import os


class Linker:

    def __init__(self, datamodel):
        self.datamodel = datamodel
        self._verbose = False

    def verbose(self):
        self._verbose = True

    def log(self, m):
        if self._verbose:
            print("[linker] " + m)

    def resolve(self, ref, current=None, parent=None):

        root = self.datamodel.root

        ref = ref.lower()
        if ref == "/project":
            if "project1" in root:
                return root["project1"]
            return None

        if ref[:2] == "./":
            if current == None:
                return None
            current = current
            ref = ref[2:]

        if ref[:3] == "../":
            if parent == None:
                if current != None:
                    parent = current.parent
            if parent == None:
                return None
            current = parent
            ref = ref[3:]

        if ref[:1] == "/":
            if "project1" in root:
                current = root["project1"]
                ref = ref[1:]

        if current == None:
            self.log("Can not find object %s --- curent in None!!!! [%s]" %
                     (ref, ref[:1]))
            return None

        self.log("Looking for %s from %s>%s" % (ref, parent, current))

        depth = 1
        selection = [current]
        for element in ref.lower().split("/"):

            self.log("+")
            self.log("+ %s" % (element))
            self.log("+")
            attributeKey = None
            attributeVal = None

            #Look for, eg "port[name=port1]" or "port[*]"
            #/port[name=Port1]/EmulatedDevice[Name=IGMP Client $item]/Ipv4If

            parts = re.findall("([a-zA-Z]+)\\[(.*?)\\]", element)
            if len(parts) == 1:
                parts = parts[0]
                attributeKey = parts[1].split("=")[0]
                attributeVal = parts[1].split("=")[1]
                element = parts[0]

            elif len(parts) != 0:
                raise Exception("reference syntax error: '%s' from '%s'" %
                                (element, ref))

            nselection = []
            for node in selection:
                for node in node.children.values():
                    attr = node.attributes
                    if not ("object_type" in attr):
                        self.log("| Checking object=%s -> No object type!!" %
                                 (node))
                        continue

                    objType = attr["object_type"]

                    # self.log("| Checkingtype=%s  attribute=%s -> looking for type '%s'"%(attr["object_type"],attributeKey,ref))

                    if objType.lower() == element:

                        if attributeKey != None:

                            if not (attributeKey in attr):
                                self.log(
                                    "| Checking object=%s -> No such attribute %s"
                                    % (node, attributeKey))
                                continue

                            if attr[attributeKey].lower() != attributeVal:
                                self.log(
                                    "| Checking object=%s -> Wrong attribute %s: %s!=%s"
                                    %
                                    (node, attributeKey,
                                     attr[attributeKey].lower(), attributeVal))
                                continue

                        self.log("| Checking object=%s -> Using it" % (node))
                        nselection.append(node)

                    else:

                        self.log("| Checking object=%s -> Wrong type" % (node))

            if len(nselection) == 0:
                self.log("| Can not find object %s from %s [%s]" %
                         (ref, current, ref[:1]))
                return None

            selection = nselection

        self.log("%s from %s -> %s" % (ref, current, selection[0]))
        return selection[0]
