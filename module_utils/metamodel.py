# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-07-13 17:01:45

try:
    from ansible.module_utils.templater import Templater
    from ansible.module_utils.datamodel import DataModel
    from ansible.module_utils.objtree import ObjectTree
    from ansible.module_utils.stcrest import StcRest
    from ansible.module_utils.tags import TagManager
    from ansible.module_utils.xpath import Linker
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.drv import DRV
    from ansible.module_utils.utils import *
except ImportError:
    from module_utils.templater import Templater
    from module_utils.datamodel import DataModel
    from module_utils.objtree import ObjectTree
    from module_utils.stcrest import StcRest
    from module_utils.tags import TagManager
    from module_utils.xpath import Linker
    from module_utils.logger import Logger
    from module_utils.drv import DRV
    from module_utils.utils import *

import requests
import pickle
import time
import json
import re

log = Logger("metamodel")


class MetaModel:

    def __init__(self, server="127.0.0.1"):
        self.datamodel = DataModel()
        self.rest = StcRest(server, self.datamodel.session())
        self.xpath = Linker(self.datamodel, self.rest)
        self.templater = Templater(self.datamodel)
        self.tagMgr = TagManager(self.rest)

    def action(self, params):

        action = params["action"]
        count = params["count"] if "count" in params else 1

        objects = params["objects"] if "objects" in params else None
        if objects == None and "object" in params:
            objects = params["object"]

        log.info("Action: %s" % json.dumps(params, indent=4))

        if action == "session":

            chassis = params["chassis"] if "chassis" in params else None
            if chassis != None and chassis != "":
                chassis = chassis.split(" ")
            else:
                chassis = []

            ports = params["ports"] if "ports" in params else None
            if ports != None and ports != "":
                try:
                    ports = resolvePorts(ports)
                    log.info("Ports: %s" % str(ports))
                except Exception as err:
                    return Result.error("Ports handling Exception: %s" % str(err))
                
            else:
                ports = []

            portNames = params["names"] if "names" in params else None
            if portNames != None and portNames != "":
                portNames = resolveNames(portNames)
                log.info("PortNames: %s" % str(portNames))
            else:
                portNames = []

            if len(ports) != 0 and len(portNames) != 0 and len(ports) != len(portNames):
                return Result.error("The number of ports and names does not match, please check")

            # print(">>> new session <<< user:%s name:%s chassis:%s" %
            #       (Color.blue(params["user"]), Color.blue(params["name"]), Color.green(str(chassis))))
            propsDict = {"ports":ports, "names":portNames}

            reset_existing = (not ("reset_existing" in params)) or (params["reset_existing"] == True)
            kill_existing = "kill_existing" in params and params["kill_existing"]
            result = self.new_session(params["user"], params["name"], chassis, propsDict, reset_existing, kill_existing)

        elif action == "create":

            under = params["under"] if "under" in params else None
            result = self.create(objects, under, count=count)

        elif action == "config":

            if type(objects) is list:
                if len(objects) != 1:
                    return Result.error("There should be only one object to configure, but there are %d: %s" %
                                        (len(objects), objects))
                objects = objects[0]
            result = self.config(params["properties"], objects, count=count)

        elif action == "perform":

            properties = params["properties"] if "properties" in params and params["properties"] != None else {}
            result = self.perform(params["command"], properties, count=count)

        elif action == "wait":

            if objects == None:
                log.error("No object specified tor get actions: %s" % params)
                return Result.error("No object specified for the wait actions: %s" % params)

            timeout = params["timeout"] if "timeout" in params and params["timeout"] != None else 60
            result = self.wait(objects, params["until"], timeout=int(timeout), count=count)

        elif action == "get":

            if objects == None:
                log.error("No object specified tor get actions: %s" % params)
                return Result.error("No object specified for the get actions: %s" % params)

            result = self.get(objects, count=count)

        elif action == "delete":

            if objects == None:
                log.error("No object specified tor get actions: %s" % params)
                return Result.error("No object specified for the get actions: %s" % params)

            result = self.delete(objects, count=count)

        elif action == "load":

            result = self.load_datamodel(params["datamodel"])

        elif action == "files":

            files = self.rest.files()
            if files == None:
                return Result.error(self.rest.errorInfo)
            return Result.value(files)

        elif action == "download":

            dest = params["dest"] if "dest" in params else "/tmp"
            files = self.rest.download(params["file"], dest)
            if files == None:
                return Result.error(self.rest.errorInfo)

            return Result.value(files)

        elif action[0:4] == "drv.":

            if objects != None:
                if type(objects) is list:
                    if len(objects) != 1:
                        return Result.error("There should be only one object, but there are %d: %s" %
                                            (len(objects), objects))
                    objects = objects[0]

                objects = self.xpath.resolveObjects(objects)

            if objects == None:
                return Result.error("Can not fetch DRV: no valid objects selected")

            drv = DRV(objects, self.rest)
            if action[4:] == "fetch":
                result = Result.value(drv.fetch())

            elif action[4:] == "subscribe":
                result = Result.value(drv.subscribe())

            else:
                result = Result.error("Unknown DRV action %s" % action[4:])

            return result

        else:

            log.error("Unknown action: %s" % action)
            result = Result.error("Unknown action %s" % action)

        # log.info("action %s result: %s" % (action, json.dumps(result.val, indent=4)))

        self.serialize()
        return result

    def dump(self):
        self.datamodel.dump()

    def serialize(self):
        self.datamodel.serialize()

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def new_session(self, user_name, session_name, chassis=[], props={"ports":[], "names":[]}, reset_existing=True, kill_existing=False):

        self.datamodel.new(session_name + " - " + user_name, chassis, props),
        if not self.rest.new_session(user_name, session_name, reset_existing, kill_existing):
            return Result.error("Failed to create a session: %s" % self.rest.errorInfo)

        if len(chassis) > 0 and not self.rest.connect(chassis):
            return Result.error("Failed to connect to the chassis: %s" % self.rest.errorInfo)

        return Result.value(1)

    def load_datamodel(self, filename):

        with open(filename) as dmfile:

            res = self.rest.perform("LoadFromXml", {
                "InputConfigString": dmfile.read(),
                "Filename": "",
            })
            if res != None:
                res["InputConfigString"] = "..."
            else:
                return Result.error(self.rest.errorInfo)

            #Then reset the data-model
            self.datamodel.reset()

            return Result.value(res)
        return "Ooops"

    def config(self, properties, objref=None, count=1):

        handles = {}
        for i in range(0, count):

            ref = self.templater.get(objref, i)
            obj = self.xpath.resolveSingleObject(ref)
            if obj == None:
                return Result.error("config: Can not find parent object %s" % ref)

            r = self.configObject(obj, self.templater.get(properties, i))
            if r.isError():
                return r

            handles[i] = r.val

        if count == 1:
            handles = handles[0]
        return Result.value(handles)

    def create(self, objects, under=None, count=1):

        handles = {}
        for i in range(0, count):

            parent = None
            if under != None:
                ref = self.templater.get(under, i)
                parent = self.xpath.resolveSingleObject(ref)
                if parent == None:
                    return Result.error("create: Can not find parent object %s" % ref)

            r = self.createObject(self.templater.get(objects, i), parent)
            if r.isError():
                return r

            handles[i] = r.val

        if count == 1:
            handles = handles[0]
        return Result.value(handles)

    def perform(self, command, properties, count=1):

        handles = {}
        name = properties["name"] if "name" in properties else ""
        userTags = properties["tag"] if "tag" in properties else ""
        for i in range(0, count):
            props = self.templater.get(properties, i)
            if command == "DeviceCreate":
                props["name"] = name
                if userTags != "":
                    props["tag"] = userTags

            r = self.performConfig(command, props)
            if r.isError():
                return r

            handles[i] = r.val

        if count == 1:
            handles = handles[0]
        return Result.value(handles)

    def delete(self, objects, count=1):

        nodes = self._getnodes(objects, count)
        if nodes.isError():
            return nodes

        handles = []
        for node in nodes.val:
            if not self.rest.delete(node.handle):
                return Result.error(self.rest.errorInfo)

            self.datamodel.deleteNode(node)
            handles.append(node.handle)

        return Result.value(handles)

    def wait(self, objects, until, timeout=60, count=1):

        nodes = self._getnodes(objects, count)
        if nodes.isError():
            return nodes

        start = time.time()
        while time.time() - start < timeout:
            failed = 0
            for node in nodes.val:
                # Evaluate the condition
                if not self.evaluateCondition(node.handle, until):
                    failed += 1
                    pass
            if failed == 0:
                break
            time.sleep(1)

        if failed > 0:
            return Result.error("[wait] failed on condition %s" % until)

        return Result.value([n.handle for n in nodes.val])

    def get(self, objects, count=1):

        nodes = self._getnodes(objects, count)
        if nodes.isError():
            return nodes

        result = {}
        isSingleton = len(nodes.val) == 1
        for node in nodes.val:
            obj = self.rest.get(node.handle)
            if isSingleton:
                result = obj
            else:
                result[node.handle] = obj

        return Result.value(result)

    def _getnodes(self, objects, count=1):
        if not type(objects) is list:
            objects = [objects]
        log.debug("Get all handles %s/%d" % (objects, count))

        nodes = []
        for i in range(0, count):
            for obj in objects:
                ref = self.templater.get(obj, i)
                selection = self.xpath.resolveObjects(ref)
                log.debug("Get all nodes [%d/%d] -> %s -> %s" % (i, count, ref, selection))
                if selection != None:
                    nodes += selection.nodes

        #ignore when no object found
        #if len(nodes) == 0:
        #    return Result.error("Can not find any object matching %s (count=%d)" % (obj, count))

        return Result.value(nodes)

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def evaluateCondition(self, handle, condition):

        match = re.findall(r"^\s*(\S+)\s*=\s*(\S+)\s*$", condition)
        if len(match) != 1:
            raise Exception("Failed to parse condition: %s" % condition)
        key = match[0][0]
        val = match[0][1]

        obj = self.rest.get(handle)

        if not (key in obj):
            raise Exception("Object %s does not have any property %s" % (obj, key))

        name = (" (" + obj["name"] + ")") if "name" in obj else ""
        log.info("[evaluate] handle %s%s key %s val %s expected %s" % (handle, name, key, obj[key], val))
        return obj[key] == val

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def performConfig(self, command, props):

        params = {}
        for key in props.keys():

            val = props[key]
            if type(val) is str and val[0:4] == "ref:":
                objects = self.xpath.resolveObjects(val)
                if objects == None:
                    return Result.error("Failed to resolve: %s" % val)
                val = " ".join(objects.handles())
            params[key] = val

        # The tags are configured with device config
        userTags = {}
        if command == "DeviceCreate":
            userTags = self.tagMgr.getPoppedTags(params)
            log.info("Pop user tags(%s) for later configuration" % str(userTags))

        result = self.rest.perform(command, params)
        if result == None:
            return Result.error(self.rest.errorInfo)

        if command != "DeviceCreate" or not ("name" in props):
            return Result.value(result)

        if not "ReturnList" in result or result["ReturnList"] == None:
            return Result.value("No handles returned!")

        handles = result["ReturnList"].split(" ")
        log.info("There are %d handles to configure" % len(handles))

        for i in range(len(handles)):
            handle = handles[i]
            newTag = self.templater.get(userTags, i)
            self.tagMgr.handleTags(newTag)

            attributes = {"name": self.templater.get(props["name"], i), "usertag-targets": newTag.get("usertag-targets", "")}
            if not self.rest.config(handle, attributes):
                return Result.error(self.rest.errorInfo)

            # Add the new object to the internal data model
            attributes["object_type"] = "EmulatedDevice"
            self.datamodel.insert(handle, attributes, self.datamodel.root["project1"])

        return Result.value(handles)

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
                    objects = self.xpath.resolveObjects(val)
                    if objects == None:
                        log.info("reference \033[92m%s\033[0m is not resolved yet" % (val))
                        references[key] = val
                        continue
                    log.info("reference \033[92m%s\033[0m resolved to %s" % (val, objects))
                    val = " ".join(objects.handles())

                params[key] = val

            obj["references"] = references

            if not isConfig:

                # print("Creating",json.dumps(params,indent=4))
                fparams = {key: value for (key, value) in params.items() if key.find(".object_type") < 0}
                # print("Creating",json.dumps(fparams,indent=4))
                if under != None:
                    # When project1 is created, if project1's children is not got, 
                    # getting children in tag1 will fail. 
                    self.rest.children("project1")
                    self.tagMgr.handleTags(fparams)

                ## DynamicResultView with the same name will be created multiple times, which cause
                ## subscription failed
                if obj["type"] == 'DynamicResultView':
                    drvName = fparams.get('name')
                    if drvName != None:
                        self.delete('ref:/project/DynamicResultView[name="%s"]' % drvName)

                handle = self.rest.create(obj["type"], fparams)
                if handle == None:
                    return Result.error(self.rest.errorInfo)

                params["object_type"] = obj["type"]
                newObject = self.datamodel.insert(handle, params, under)

                log.info("New object created. Handle %s props %s" % (handle, json.dumps(params, indent=4)))

                newObjects[obj["type"]] = newObject
                obj["object"] = newObject
                obj["under"] = under

                if obj["type"].lower() == "port" and "name" in params and "location" in params:
                    log.info("Port %s created with location %s -> handle %s" %
                             (Color.green(params["name"]), Color.green(params["location"]), Color.blue(handle)))

            else:

                # Remove the "object_type" property has it can fail
                fparams = {key: value for (key, value) in params.items() if key.find("object_type") < 0}
                if not self.rest.config(parent.handle, fparams):
                    return Result.error(self.rest.errorInfo)
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
                newObject = self.datamodel.insert(handle, params, obj["object"])

                log.info("New child object added. Handle %s props %s" % (handle, json.dumps(params, indent=4)))

            #Check for any new children which was added with beeing queried
            for handle in children:
                if not handle in obj["object"].children:
                    otype = re.sub(r'^(.*?)([0-9]*)$', r'\1', handle)
                    params = {"object_type": otype, "!discovered": True}
                    newObject = self.datamodel.insert(handle, params, obj["object"])

        # ---- Step 3: resolve the references

        for obj in tree.objects:

            config = {}
            refs = obj["references"]
            for key in refs.keys():

                val = refs[key]
                objects = self.xpath.resolveObjects(val, obj["object"])
                if objects == None:
                    log.error("Failed to resolve '\033[91m%s\033[0m' for property %s in %s" % (val, key, obj["object"]))
                    continue

                config[key] = " ".join(objects.handles())
                log.info("Reference '\033[92m%s\033[0m' resolved to %s" % (val, objects))

            if config != {}:
                if not self.rest.config(obj["object"].handle, config):
                    return Result.error(self.rest.errorInfo)

        handles = []
        for obj in tree.objects:
            handles.append(obj["object"].handle)

        return Result.value(handles)

