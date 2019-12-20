# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2019-12-20 14:09:55

try:
    from ansible.module_utils.datamodel import DataModel
except ImportError:
    from datamodel import DataModel

import requests
import pickle
import json
import re

class MetaModel:

    def __init__(self, server="127.0.0.1"):  
        self.datamodel = DataModel()
        self.server= server
        self.errorInfo = None
        self._verbose = False  

    def verbose(self):
        self.datamodel.verbose() 
        self._verbose = True 

    def log(self,m):
        if self._verbose:
            print(m)


    def serialize(self):
        self.datamodel.serialize()

    def new_session(self, user_name,session_name):

        self.datamodel.new(session_name+" - "+user_name),

        url = "http://"+self.server+"/stcapi/sessions"
        params = {'userid': user_name, 'sessionname': session_name}
        rsp = requests.post(url,  headers={'Accept': 'application/json'}, data=params, timeout=30)
        if rsp.status_code == 409 or rsp.status_code == 200:
            return None
        return "Failed to create session: "+rsp.content


    def config(self,properties,objref=None):

        # self.verbose()
        obj = self.datamodel.resolve(objref[4:])
        if obj==None:
            raise Exception("Can not find parent object %s"%objref)

        return self.configObject(obj,properties)

    def create(self,objects,under=None):

        parent = None
        if under!=None:
            parent = self.datamodel.resolve(under[4:])
            if parent==None:
                raise Exception("Can not find parent object "+under)

        return self.createObject(objects,{},parent)



    # --------------------------------------------------------------------

    def configObject(self, obj, attributes): 

        config = {} 
        children = {}
        knownrefs = {}
        references = {}

        # print("config:",json.dumps(attributes,indent=4))

        for key in attributes.keys():
            val = attributes[key]
            if key == "children":
                pass

            elif type(val) is list:
                children[key]=val

            elif type(val) is str:
                if val[0:4]=="ref:":
                    ref = val[4:]
                    val = self.datamodel.resolve(ref,obj)
                    if val==None:
                        references[key]=ref
                        continue
                    knownrefs[key]=val
                    val = val.handle
                config[key]=val

            elif type(val) is dict:
                children[key]=val

            elif type(val) is int:
                config[key]=val

            else:
                print("++What is...",key, val)


        obj.config(config)
        obj.config(knownrefs)

        # Two steps: crete the object first

        toconfigure = {}
        for key in children.keys():
            #Check if the child exists first
            child=  obj.hasChild(key)
            # print("[config] %s->%s"%(key,child))
            if child==None:
                self.createObject(key,children[key], obj)
            else:
                toconfigure[key]=children[key]
 
         # Two steps: and then configure the existing objects

        for key in toconfigure.keys():
            self.configObject(obj.hasChild(key),toconfigure[key])

        config = {}
        updated = False
        for attr in references.keys():
            ref = references[attr]
            val = self.datamodel.resolve(ref,obj)
            if val == None:
                raise Exception("[config] Failed to resolve reference '%s:%s' for object %s: %s"%(attr,ref,obj,self.errorInfo))
            config[attr]=val.handle
            updated = True


        if updated:
            obj.config(config)
            self._put("objects/"+obj.handle,config)

        if self._verbose:
            self.datamodel.dump()


    # --------------------------------------------------------------------

    def createObject(self, obj, attributes={}, parent=None): 

        if type(obj) is dict:

            handle = None
            for key in obj.keys():
                handle = self.createObject(key, obj[key], parent)
            return handle


        if type(obj) is list:

            handle = None
            for key in obj:
                handle = self.createObject(key, None, parent)
            return handle

        if type(attributes) is list:

            handle = self.createObject(obj,{},parent)
            for obj in attributes: 
                self.createObject(obj, {}, handle)
            return handle

        params = {}
        params["object_type"]=obj
        if parent!=None:
            params["under"]=parent.handle

        children = {}
        knownrefs = {}
        references = {}
        for key in attributes.keys():
            val = attributes[key]
            if key == "children":
                pass

            elif type(val) is list:
                # print("++Skipping...",key)
                children[key]=val

            elif type(val) is str:
                if val[0:4]=="ref:":
                    ref = val[4:]
                    val = self.datamodel.resolve(ref,None,parent)
                    # print("++Resolving...",ref,"->",val)
                    if val==None:
                        references[key]=ref
                        continue
                    knownrefs[key]=val
                    val = val.handle
                params[key]=val

            elif type(val) is dict:
                # print("++Skipping...",key)
                children[key]=val

            elif type(val) is int:
                params[key]=val

            else:
                print("++What is...",key, val)


        handle = self._post("objects", params)
        if handle == None:
            raise Exception("Failed to create object '%s' under %s with args %s [%s]"%(obj,parent,params,self.errorInfo))


        newObject = self.datamodel.insert(handle,params,parent)
        newObject.config(knownrefs)

        for key in children.keys():
            self.createObject(key,children[key], newObject)


        config = {}
        updated = False
        for attr in references.keys():
            ref = references[attr]
            val = self.datamodel.resolve(ref,newObject,parent)
            if val == None:
                raise Exception("Failed to resolve reference '%s:%s' for object %s: %s"%(attr,ref,newObject,self.errorInfo))
            config[attr]=val.handle
            updated = True


        if updated:
            newObject.config(config)
            self._put("objects/"+newObject.handle,config)
            # self.datamodel.dump()


        return newObject

    # --------------------------------------------------------------------

    def _get(self, container):
        url = "http://"+self.server+"/stcapi/"+container
        rsp = requests.get(url, 
            headers={'Accept': 'application/json', "X-STC-API-Session": self.datamodel.session()},
            timeout=30)

        if rsp.status_code == 200:
            self.errorInfo = None
            return rsp.json()
        else:
            self.errorInfo = "failed - url:%s - code:%d - content:%s!"%(url,rsp.status_code,rsp.content)
            return "!"+url+":"+str(rsp.content)

    def _put(self, container, params):
        url = "http://"+self.server+"/stcapi/"+container
        rsp = requests.put(url, 
            headers={'Accept': 'application/json', "X-STC-API-Session": self.datamodel.session()},
            data=params, 
            timeout=30)

        if rsp.status_code == 200:
            self.errorInfo = None
            return rsp.json()
        else:
            self.errorInfo = "failed - url:%s - code:%d - content:%s - params:%s!"%(url,rsp.status_code,rsp.content,params)
            return None

    def _post(self, container, params = {}):
        url = "http://"+self.server+"/stcapi/"+container
        rsp = requests.post(url, 
            headers={'Accept': 'application/json', "X-STC-API-Session":self.datamodel.session()},
            data=params, 
            timeout=30)

        if rsp.status_code == 200 or rsp.status_code == 201:
            self.errorInfo = None
            body = rsp.json()
            # print(">>>>",body)
            return body["handle"]
        elif rsp.status_code == 500:
            body = rsp.json()
            if body["code"]==1001:
                #STC exception: in create: Unable to add PppoeServerIpv4PeerPool 23 to PppoeServerBlockConfig 15 due to max relation constraint limit : 1
                props = self._get(container+"/"+params["under"])
                t = params["object_type"].lower()
                for child in props["children"].split(" "):
                    if child[:len(t)]==t:
                        return child

        self.errorInfo = "post failed\n - url:%s\n - code:%d\n - content:%s\n - params:%s!"%(url,rsp.status_code,rsp.content,params)
        print(self.errorInfo)
        return None

    def error(self):
        return self.errorInfo

def isSimpleObject(d):
    for k in d.keys():
        v = d[k]
        if type(v) is str:
            if v[:4]=="ref:":
                return False
        elif type(v) is int:
            continue
        else:
            return False
    return True


