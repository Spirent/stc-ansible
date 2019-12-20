# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2019-12-20 14:02:26

import requests
import pickle
import json
import re

class ObjectModel:

    def __init__(self,handle,attributes,parent):  
        self.handle = handle
        self.children = {}
        self.attributes = attributes
        self.parent = parent

    def __str__(self):
        name = ""
        if "name" in self.attributes:
            name = ": "+self.attributes["name"]
        return "(\033[92m"+self.handle+"\033[0m"+name+")"

    def dump(self,prefix=""):
        s= "\033[91m"+self.handle+"\033[0m"
        for key in self.attributes:
            if key =="object_type" or key=="under":
                continue
            s+=prefix+"%s=%s"%(key,self.attributes[key])
        return s

    def config(self,model):
        for attr in model.keys():
            self.attributes[attr]=model[attr] 

    def hasChild(self, objtype):
        for handle in self.children:
            child = self.children[handle]
            if child.attributes["object_type"]==objtype:
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
            elif not ((type(val) is str) or (type(val) is int) or (type(val) is unicode)):
                val = val.handle
            attributes[attr]=val

        handles[self.handle]={
            "attributes":attributes,
            "children":children
        }

        return handles

    def unserialize(self, model):
        for child in model[self.handle]["children"]:
            node = ObjectModel(child,model[child]["attributes"],self)
            node.unserialize(model)
            self.children[child]=node



class DataModel:

    def __init__(self):
        self._session = None
        self._verbose = False  
        self.unserialize()

    def verbose(self):
        self._verbose = True  

    def log(self,m):
        if self._verbose:
            print(m)

    def session(self):
        return self._session


    def new(self, session):
        self._session =session
        self.root= {}


    def unserialize(self):
        self.root = {}
        try:
            filename = "stc-ansible-datamodel.json"
            with open(filename) as json_file:
                model = json.load(json_file)

                self._session =  model["session"]
                project1 = model["model"]["project1"]
                project = ObjectModel("project1",project1["attributes"],None)
                project.unserialize(model["model"])
                self.root["project1"]=project
                
        except Exception as error:
            self.root = {}
        #self.dump()

    def serialize(self):

        filename = "stc-ansible-datamodel.json"
        with open(filename, 'w') as outfile:
            data = {"model":{},"session":self._session}
            if "project1" in self.root:
                data["model"]=self.root["project1"].serialize()
            json.dump(data, outfile, indent=4)

    def dump(self, node=None, level=0):

        if node==None:
            print("----------")
            node = self.root
        prefix = "| "*(level+1)
        for key in node.keys():
            print("%s%s"%(prefix,node[key].dump("\n"+prefix+"-")))
            self.dump(node[key].children,level+1)

    def insert(self, handle, attributes, parent=None):

        obj = ObjectModel(handle,attributes,parent)

        nodes = self.root
        if parent != None:
            nodes = parent.children

        if handle in nodes:
            self.log("[data-model] Object %s already exists..."%obj)
            return nodes[handle]

        nodes[handle]=obj


        self.log("[data-model] Inserting object '%s' under %s"%(obj,parent))

        return obj

    def resolve(self, ref, current=None, parent=None):

        ref = ref.lower()
        if ref=="/project":
            return self.root["project1"]

        # self.log("[resolver] Looking for %s from %s>%s"%(ref,parent,current))

        if ref[:2] == "./":
            if current == None:
                return None
            current = current.children
            ref = ref[2:]

        if ref[:3] == "../":
            if parent == None:
                if current != None:
                    parent = current.parent
            if parent == None:
                return None
            current = parent.children
            ref = ref[3:]

        if ref[:1] == "/":
            current = self.root["project1"].children
            ref = ref[1:]

        if current == None:
            # self.log("[resolver] Can not find object %s --- curent in None!!!! [%s]"%(ref,ref[:1]))
            return None

        parts = re.findall("([a-zA-Z]+)\\[(.*?)=(.*?)\\]", ref)
        if len(parts)==1:
            parts = parts[0]
            ref=parts[0]

        obj = None
        for key in current.keys():
            node = current[key]
            attr = node.attributes

            # self.log("[resolver] Checking %s/%s [looking for %s]"%(key,attr["object_type"],ref))
            if attr["object_type"].lower()==ref:
                if len(parts)==3 and not (parts[1] in attr and attr[parts[1]].lower()==parts[2]):
                    # self.log("[resolver] Checking %s/%s -> Invalid attribute %s:%s != %s"% 
                        # (key,attr["object_type"],parts[1],attr[parts[1]],parts[2]))
                    continue
                obj = node


        if obj != None:
            self.log("[resolver] %s from %s -> %s"%(ref,current,obj))
            return obj

        self.log("[resolver] Can not find object %s from %s [%s]"%(ref,current,ref[:1]))

        return None


