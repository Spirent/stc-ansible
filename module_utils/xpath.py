# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-07-13 15:17:13

try:
    from ansible.module_utils.logger import Logger
except ImportError:
    from module_utils.logger import Logger

import requests
import json
import re
import os
from functools import cmp_to_key

log = Logger("linker")


class Linker:

    def __init__(self, datamodel, rest=None):
        self.datamodel = datamodel
        self.rest = rest

    def resolveSingleObject(self, ref):

        selection = self._resolve(ref)
        if selection == None:
            return

        if selection != None and selection.count() > 1:
            raise Exception("There are too many choices for reference %s: %s" % (ref, selection))

        return selection.firstNode()

    def resolveObjects(self, ref, current=None):
        myrefs = re.split(",|;", ref)
        myselections = NodeSelector()
        for myref in myrefs:
            if myref.strip() == "":
                continue
            selection = self._resolve(myref, current)
            if selection != None and selection.count() > 0:
                myselections.extendex(selection)
        if myselections.count() == 0:
            return None
        return myselections

    def _resolve(self, ref, current=None):
        if ref == None:
            return None

        if ref[0:4] == "ref:":
            ref = ref[4:]
        root = self.datamodel.root

        ref = ref.lower()
        if ref[:2] == "./":
            if current == None:
                return None
            current = current
            ref = ref[2:]

        elif ref[:3] == "../":
            if current == None:
                print("Trying to resolve %s ... but current is None!" % ref)
                return None
            if current.parent == None:
                print("Trying to resolve %s ... but current's parent is None!" % ref)
                return None
            print("Resolve(%s): Using parent %s for object %s" % (ref, current.parent, current))
            current = current.parent
            ref = ref[3:]

        elif ref[:8] == "/project":
            current = self.datamodel.getRoot("project")
            ref = ref[8:]

        elif ref[:7] == "/system":
            current = self.datamodel.getRoot("system")
            ref = ref[7:]

        elif ref[:1] == "/":
            current = self.datamodel.getRoot("project")
            ref = ref[1:]

        elif ref[:3] == "? /":
            current = self.datamodel.getRoot("project")
            ref = ref[3:]

        else:
            log.warning("Invalid reference syntax: '%s'" % (ref))
            return None

        if current == None:
            log.warning("Can not find object %s --- curent in None!!!! [%s]" % (ref, ref[:1]))
            self.datamodel.dump()
            return None

        if len(ref) > 0 and ref[0] == "/":
            ref = ref[1:]

        if len(ref) == 0:
            return NodeSelector(current)

        log.info("Looking for %s from %s" % (ref, current))

        hasWildcard = False
        selection = NodeSelector(current)

        for element in ref.lower().split("/"):

            #Look for, eg "port[name=port1]" or "port[*]"
            #/port[name=Port1]/EmulatedDevice[*]/Ipv4If

            selector = Selector(element)
            self.discoverChildren(selection, selector.element)

            if selection.select(selector) == 0:
                log.warning("| Can not find object %s from %s [%s]" % (ref, current, ref[:1]))
                return None

        log.info("%s from %s -> %s" % (ref, current, selection))
        return selection

    def discoverChildren(self, selection, object_type):

        if self.rest == None:
            return

        for node in selection.nodes:

            if len(node.children) != 0 and node.hasChild(object_type):
                log.debug("[dicovering] node %s already has children" % (node))
                continue

            children = self.rest.children(node.handle)
            if len(children) == 0:
                log.debug("[dicovering] node %s has no children" % (node))
                continue

            log.info("[dicovering] node %s 's children are %s." % (node, children))

            for handle in children:
                if handle in node.children:
                    continue
                attr = self.rest.get(handle)
                # Convert attr keys to lower case
                attr = dict((k.lower(), v) for k, v in attr.items())
                attr["object_type"] = re.sub(r'^(.*?)([0-9]*)$', r'\1', handle)
                self.datamodel.insert(handle, attr, node)


class NodeSelector:

    def __init__(self, node=None):
        if node == None:
            self.nodes = []
        else:
            self.nodes = [node]

    def log(self, m):
        log.debug("[selector] " + m)

    def __str__(self):
        s = ""
        for node in self.nodes:
            s += "," if len(s) > 0 else ""
            s += str(node)
        return "[" + s + "]"

    def count(self):
        return len(self.nodes)

    def get(self, n):
        return self.nodes[n]

    def firstNode(self):
        return self.nodes[0]

    def handles(self):
        return [n.handle for n in self.nodes]

    def select(self, selector):

        self.nodes = selector.filterNodes(self.nodes)
        return len(self.nodes)

    def isDifferent(self, other):
        if other != None:
            if self.nodes == other.nodes:
                return False
            if len(other.nodes) == 0:
                return len(self.nodes) > 0

            for n in other.nodes:
                if n not in self.nodes:
                    return True
            return False
        return True

    def extend(self, other):
        if other != None:
            for n in other.nodes:
                if n not in self.nodes:
                    self.nodes.append(n)

    #requires the duplicate like: 
    #ipv4netwokblock1 ipv4netwokblock2 ipv4netwokblock1 ipv4netwokblock2
    def extendex(self, other):
        if other != None:
            for n in other.nodes:
                self.nodes.append(n)
                
    def intersect(self, other):
        new = NodeSelector()
        if other != None:
            for n in other.nodes:
                if n in self.nodes:
                    new.nodes.append(n)
        return new


class Selector:

    indexing = 1
    equal = 2
    different = 3
    contains = 4
    startswith = 5

    def __init__(self, element):

        #a[contains(@href, '://')]
        match = re.findall("^(\\w+|\\*)\\s*(\\[.*\\])?\\s*$", element)
        if len(match) != 1:
            raise Exception("[xpath] Syntax error with selector '%s'" % element)

        selectors = []
        self.element = match[0][0]
        for selector in re.findall("\\[\\s*@?(.*?)\\s*\\]", match[0][1]):

            if re.search("^[0-9]*$", selector):
                selectors.append({"type": Selector.indexing, "val": int(selector)})
                continue

            if re.search("^\\s*\\*\\s*$", selector):
                #Legacy selector
                continue

            operators = {
                "=": Selector.equal,
                "!=": Selector.different,
                "\\*=": Selector.contains,
                "\\~=": Selector.contains,
                "\\^=": Selector.startswith,
            }

            found = False
            for operator, id in operators.items():
                matcher = "^(\\w+)\\s*" + operator + "\\s*(.*)$"
                if re.search(matcher, selector) != None:

                    match = re.findall(matcher, selector)
                    value = match[0][1]
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    if value.startswith("\"") and value.endswith("\""):
                        value = value[1:-1]
                    selectors.append({"type": id, "val": value, "key": match[0][0]})
                    found = True
                    break

            if not found:
                raise Exception("[xpath] Syntax error with expression '%s' selector: '%s'" % (element, selector))

        log.debug("Selector %s -> %s" % (element, selectors))
        self.selectors = selectors
    
    #comparing the handles like: router9 router11 based on the number in the handle
    #to sort on the number in the handle, the ascending sort is : router9 router11
    #to sort in dictionary, the ascending sort is : router11 router9
    def cmp_handle(self, item1, item2):
        obj1 = item1.handle
        obj2 = item2.handle
        objType = re.sub(r'\d+$', "", obj1)
        len1 = len(objType)
        log.debug("cmp_handle-- %s, %s" % (obj1, objType))
        if int(obj1[len1:]) > int(obj2[len1:]):
            return 1
        elif int(obj1[len1:]) < int(obj2[len1:]):
            return -1
        return 0

    def filterNodes(self, nodes):

        selection = []

        log.debug("Selector: filtering %s" % [str(n) for n in nodes])

        for node in nodes:

            for node in node.children.values():

                if self.element != "*":

                    if not ("object_type" in node.attributes):
                        self.log("| Checking object=%s -> No object type!!" % (node))
                        continue

                    objType = node.attributes["object_type"].lower()

                    # Special case for inheritance handling
                    if objType == "router" and self.element == "emulateddevice":
                        objType = "emulateddevice"

                    if objType != self.element:
                        continue

                selection.append(node)

        log.debug("Selector: candidates are %s" % [str(n.handle) for n in selection])
        # sort handles to get correct order
        selection.sort(key=cmp_to_key(self.cmp_handle))

        for selector in self.selectors:

            # oselection = selection
            if selector["type"] == Selector.indexing:
                idx = selector["val"]
                if idx < len(selection) and idx >= 0:
                    selection = [selection[idx]]
                else:
                    selection = []
            else:
                selection = [node for node in selection if self.checkSelector(selector, node)]

            # log.debug("Selector: %s: %s -> %s" % (selector, oselection, selection))

        return selection

    def checkSelector(self, selector, node):

        attr = node.attributes
        attrKey = selector["key"]
        if not (attrKey in attr):
            log.debug("| Checking object=%s -> No such attribute %s %s" % (node, attrKey, attr.keys()))
            return False

        isValid = False
        selectorValue = selector["val"]
        value = str(attr[attrKey]).lower()
        if selector["type"] == Selector.equal:
            if attr["object_type"] == "port":
                isValid = ((value == selectorValue) or
                           (re.sub(r"\s//.*", "", value) == re.sub(r"\s//.*", "", selectorValue)))
            else:
                isValid = (value == selectorValue)

        elif selector["type"] == Selector.different:

            isValid = (value != selectorValue)

        elif selector["type"] == Selector.contains:

            isValid = (value.find(selectorValue) >= 0)

        elif selector["type"] == Selector.startswith:

            isValid = (value.find(selectorValue) == 0)

        log.debug("Node %s: %s (%s/%s)" % (node, isValid, value, selectorValue))
        return isValid
