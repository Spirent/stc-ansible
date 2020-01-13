# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-13 16:19:38

try:
    from ansible.module_utils.templater import Templater
    from ansible.module_utils.datamodel import DataModel
    from ansible.module_utils.objtree import ObjectTree
    from ansible.module_utils.stcrest import StcRest
    from ansible.module_utils.linker import Linker
except ImportError:
    from module_utils.templater import Templater
    from module_utils.datamodel import DataModel
    from module_utils.objtree import ObjectTree
    from module_utils.stcrest import StcRest
    from module_utils.linker import Linker

import requests
import pickle
import time
import json
import re


class MetaModel:
    def __init__(self, server="127.0.0.1"):
        self.datamodel = DataModel()
        self.linker = Linker(self.datamodel)
        self._verbose = False
        self.rest = StcRest(server, self.datamodel.session())

    def verbose(self):
        #self.datamodel.verbose()
        self.rest.verbose()
        self._verbose = True

    def action(self, params):

        action = params["action"]
        if action == "new_session":

            result = self.new_session(params["user"], params["name"])

        elif action == "create":

            under = params["under"] if "under" in params else None
            count = params["count"] if "count" in params else 1

            result = self.create(params["objects"], under, count=count)

        elif action == "config":

            parent = params["object"] if "object" in params else None
            count = params["count"] if "count" in params else 1

            result = self.config(params["properties"], parent, count=count)

        elif action == "perform":

            count = params["count"] if "count" in params else 1
            result = self.perform(params["command"],
                                  params["properties"],
                                  count=count)

        elif action == "load":

            result = self.load_datamodel(params["datamodel"])

        else:

            raise Exception("Unknown action " + action)

        self.serialize()
        return result

    def dump(self):
        self.datamodel.dump()

    def serialize(self):
        self.datamodel.serialize()

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def log(self, m):
        if self._verbose:
            print(m)

    def new_session(self, user_name, session_name):
        self.datamodel.new(session_name + " - " + user_name),
        return self.rest.new_session(user_name, session_name)

    def load_datamodel(self, filename):

        with open(filename) as dmfile:
            dm = dmfile.read()
            res = self.rest.perform("LoadFromXml", {
                "InputConfigString": dm,
                "Filename": "",
            })
            if res != None:
                res["InputConfigString"] = "..."
            return res
        return "Ooops"

    def config(self, properties, objref=None, count=1):

        handles = {}
        for i in range(0, count):

            ref = Templater(objref[4:]).instance(i)
            obj = self.linker.resolve(ref)
            if obj == None:
                raise Exception("Can not find parent object %s" % ref)

            handles[i] = self.configObject(obj,
                                           Templater(properties).instance(i))
        return handles

    def create(self, objects, under=None, count=1):

        handles = {}
        xobjects = Templater(objects)
        for i in range(0, count):

            parent = None
            if under != None:
                ref = Templater(under[4:]).instance(i)
                parent = self.linker.resolve(ref)
                if parent == None:
                    raise Exception("Can not find parent object %s" % parent)

            # print(i,">",json.dumps(xobjects.instance(i),indent=4),"<<",json.dumps(objects,indent=4))
            handles[i] = self.createObject(xobjects.instance(i), parent)
        return handles

    def perform(self, command, properties, count=1):

        handles = {}
        name = properties["name"] if "name" in properties else ""
        for i in range(0, count):
            props = Templater(properties).instance(i)
            if command == "DeviceCreate":
                props["name"] = name
            handles[i] = self.performConfig(command, props)

        return handles

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def performConfig(self, command, props):

        params = {}
        for key in props.keys():

            val = props[key]
            if type(val) is str and val[0:4] == "ref:":
                nobj = self.linker.resolve(val[4:])
                if nobj == None:
                    raise Exception("Failed to resolve: %s" % val)
                val = nobj.handle
            params[key] = val

        result = self.rest.perform(command, params)
        if command != "DeviceCreate" or not ("name" in props):
            return result

        handles = result["ReturnList"].split(" ")
        print("There are %d handles to configure" % len(handles))
        name = Templater(props["name"])
        for i in range(len(handles)):
            handle = handles[i]
            attributes = {"name": name.instance(i)}
            self.rest.config(handle, attributes)
            # Add the new object to the internal data model

            attributes["object_type"] = "EmulatedDevice"
            self.datamodel.insert(handle, attributes,
                                  self.datamodel.root["project1"])

        return handles

        # self.datamodel.dump()

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def configObject(self, root, properties):

        objects = [{root.objectType(): properties}]
        return self.createOrConfigObject(objects, root, True)

    def createObject(self, objects, parent):

        return self.createOrConfigObject(objects, parent, False)

    # --------------------------------------------------------------------

    def createOrConfigObject(self, objects, parent, isConfig):

        tree = ObjectTree(objects)
        # if self._verbose:
        # print("Creating:",parent,json.dumps(tree.objects,indent=4))

        # ---- Step 1: create all objects

        newObjects = {}
        for obj in tree.objects:
            props = obj["props"]
            references = {}

            params = {}
            if not isConfig:
                under = parent
                if "under" in obj:
                    under = newObjects[obj["under"]]
                if under != None:
                    params["under"] = under.handle

            for key in props.keys():

                val = props[key]
                if type(val) is str and val[0:4] == "ref:":
                    nobj = self.linker.resolve(val[4:])
                    if nobj == None:
                        references[key] = val[4:]
                        continue
                    if self._verbose:
                        print("Reference \033[92m" + val + "\033[0m-->",
                              nobj.handle)
                    val = nobj.handle
                # print(type(val),":",key,val)
                params[key] = val

            obj["references"] = references

            if not isConfig:

                # print("Creating",json.dumps(params,indent=4))
                fparams = {
                    key: value
                    for (key, value) in params.items()
                    if key.find(".object_type") < 0
                }
                # print("Creating",json.dumps(fparams,indent=4))
                handle = self.rest.create(obj["type"], fparams)

                params["object_type"] = obj["type"]
                newObject = self.datamodel.insert(handle, params, under)
                if self._verbose:
                    print("\033[91m" + handle + "\033[0m-->",
                          json.dumps(params, indent=4))

                newObjects[obj["type"]] = newObject
                obj["object"] = newObject
                obj["under"] = under

            else:

                # Remove the "object_type" property has it can fail
                fparams = {
                    key: value
                    for (key, value) in params.items()
                    if key.find("object_type") < 0
                }
                handle = self.rest.config(parent.handle, fparams)
                obj["object"] = parent

        # print("children:", json.dumps(obj["children"], indent=4))

        # ---- Step 2: learn the children handles

        for obj in tree.objects:
            children = self.rest.children(obj["object"].handle)
            # print("Learning children for %s: %s" %
            #       (obj["object"].handle, children))
            for key in obj["children"]:

                if key.find(".") >= 0:
                    continue
                childid = key.lower()
                found = False
                for handle in children:
                    if handle[0:len(childid)] == childid:
                        found = True
                        break
                if not found:
                    # print("Failed to find handle for child", key, "from",
                    #       children)
                    continue

                params = obj["children"][key]
                params["object_type"] = key
                newObject = self.datamodel.insert(handle, params,
                                                  obj["object"])
                if self._verbose:
                    print("\033[91m" + handle + "\033[0m-->",
                          json.dumps(params, indent=4))

            #Check for any new children which was added with beeing queried
            for handle in children:
                if not handle in obj["object"].children:
                    otype = re.sub(r'^(.*?)([0-9]*)$', r'\1', handle)
                    params = {"object_type": otype, "!discovered": True}
                    newObject = self.datamodel.insert(handle, params,
                                                      obj["object"])

        # ---- Step 3: resolve the references

        # self.datamodel.verbose()
        for obj in tree.objects:

            config = {}
            refs = obj["references"]
            for key in refs.keys():

                val = refs[key]
                nobj = self.linker.resolve(val, obj["object"], parent)
                if nobj == None:
                    print("Reference \033[91m" + val + "\033[0m failure (",
                          key, ")")
                    continue

                config[key] = nobj.handle
                if self._verbose:
                    print("Reference \033[92m" + key + "\033[0m-->",
                          nobj.handle)

            if config != {}:
                self.rest.config(obj["object"].handle, config)

        handles = []
        for obj in tree.objects:
            handles.append(obj["object"].handle)
        return handles
