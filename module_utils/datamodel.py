# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-02-07 11:05:55

try:
    from ansible.module_utils.logger import Logger
except ImportError:
    from module_utils.logger import Logger

import requests
import pickle
import json
import re
import os

log = Logger("data-model")


class DataModel:

    def __init__(self):
        self._session = None
        self.chassis = []
        self.ports = []
        self.unserialize()

    def session(self):
        return self._session

    def new(self, session, chassis, ports):
        self._session = session
        self.chassis = chassis
        self.ports = ports
        self.reset()

    def getChassis(self, i):
        if i < len(self.chassis):
            return self.chassis[i]

    def getPorts(self, i):
        if i < len(self.ports):
            return self.ports[i]

    def getRoot(self, objtype):
        node = objtype + "1"
        if not (node in self.root):
            self.root[node] = ObjectModel(node, {"object_type": objtype}, None)
        return self.root[node]

    def reset(self):
        self.root = {}

    def unserialize(self):
        self.root = {}
        try:
            filename = "model-temp/stc-ansible-datamodel.json"
            with open(filename) as json_file:
                model = json.load(json_file)

                self._session = model["session"]
                self.chassis = model["chassis"]
                self.ports = model["ports"]
                project1 = model["model"]["project1"]
                project = ObjectModel("project1", project1["attributes"], None)
                project.unserialize(model["model"])
                self.root["project1"] = project

        except Exception as error:
            self.root = {}
        #self.dump()

    def serialize(self):

        if not os.path.exists("model-temp/"):
            os.mkdir("model-temp/")

        filename = "model-temp/stc-ansible-datamodel.json"
        with open(filename, 'w') as outfile:
            data = {"model": {}, "session": self._session, "chassis": self.chassis, "ports": self.ports}
            if "project1" in self.root:
                data["model"] = self.root["project1"].serialize()
            json.dump(data, outfile, indent=4)

    def tree(self):

        return root["project1"].serialize()

    def dump(self, node=None, level=0):

        if node == None:
            print("----------")
            node = self.root
        prefix = "| " * (level + 1)
        for key in node.keys():
            print("%s%s" % (prefix, node[key].dump("\n" + prefix + "-")))
            self.dump(node[key].children, level + 1)

    def insert(self, handle, attributes, parent=None):

        if not ("object_type" in attributes):
            raise Exception("Trying to insert handle %s without object_type attribute" % handle)
        # print("[data-model] Inserting %s (%s) under [%s]"%(handle,attributes["object_type"],parent))
        obj = ObjectModel(handle, attributes, parent)

        nodes = self.root
        if parent != None:
            nodes = parent.children

        if handle in nodes:
            log.info("[data-model] Object %s already exists..." % obj)
            return nodes[handle]

        nodes[handle] = obj

        log.info("[data-model] Inserting object '%s' under %s" % (obj, parent))

        return obj

    def deleteNode(self, node):

        if node.parent != None:
            node.parent.children.pop(node.handle)


class ObjectModel:

    def __init__(self, handle, attributes, parent):
        # Make sure to always store the attributed keys to lowercase
        attributes = {key.lower(): value for (key, value) in attributes.items()}
        self.handle = handle
        self.children = {}
        self.attributes = attributes
        self.parent = parent

    def __str__(self):
        name = ""
        if "name" in self.attributes:
            name = ": " + self.attributes["name"]
        return "(\033[92m" + self.handle + "\033[0m" + name + ")"

    def dump(self, prefix=""):
        s = "\033[91m" + self.handle + "\033[0m"
        for key in self.attributes:
            if key == "object_type" or key == "under":
                continue
            s += prefix + "%s=%s" % (key, self.attributes[key])
        return s

    def objectType(self):
        return self.attributes["object_type"]

    def config(self, model):
        for attr in model.keys():
            self.attributes[attr] = model[attr]

    def hasChild(self, objtype):
        for handle in self.children:
            child = self.children[handle]
            if child.attributes["object_type"] == objtype:
                return child
        return None

    def serialize(self, handles={}):

        children = []
        for handle in self.children.keys():

            child = self.children[handle]
            child.serialize(handles)
            children.append(handle)

        attributes = {}
        for attr in self.attributes.keys():
            val = self.attributes[attr]
            if type(val) is ObjectModel:
                val = val.handle
            elif type(val) is dict:
                try:
                    val = val.handle
                except:
                    pass
            attributes[attr] = val

        handles[self.handle] = {"attributes": attributes, "children": children}

        return handles

    def unserialize(self, model):
        for child in model[self.handle]["children"]:
            node = ObjectModel(child, model[child]["attributes"], self)
            node.unserialize(model)
            self.children[child] = node
