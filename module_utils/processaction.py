
try:
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.utils import *
except ImportError:
    from module_utils.logger import Logger
    from module_utils.utils import * 


import functools
import re

log = Logger("processaction")

class MapWorker:
    _tags = None
    def __init__(self, module_name, method_name):
        self._module = re.sub(r'.*\.', '', module_name)
        self._method = method_name
        _xpath_worker = None
    
    def pre_process(self, *args, **kwargs):
        try:
            pre_func = getattr(self, "pre_"+self._module+"_"+self._method, None)
            if pre_func != None:
                return pre_func(*args, **kwargs)
        except Exception as e:
            log.debug("worker: pre_process %s" % str(e))
        log.debug("worker: without pre_%s" % self._method)

    def post_process(self, ret, *args, **kwargs):
        try:
            post_func = getattr(self, "post_"+self._module+"_"+self._method, None)
            if post_func != None:
                return post_func(ret, *args, **kwargs)
        except Exception as e:
            log.debug("worker: post_process %s" % str(e))
        log.debug("worker: without post_%s" % self._method)

    def pre_metamodel_action(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_action")
        params = args[1]
        action = params["action"]     
        if action == "create":
            objects = params["objects"] if "objects" in params else None
            if objects == None and "object" in params:
                objects = params["object"]
            bcreatesession = False
            for objdict in objects:
                if 'session' in objdict:
                    params['action'] = 'session'
                    params['user'] = objdict['session']['user']
                    params['name'] = objdict['session']['name']
                    params['chassis'] = objdict['session']['chassis']
                    bcreatesession = True
                    break
            if bcreatesession:
                if "objects" in params: 
                    del params['objects'] 
                if "object" in params: 
                    del params['object'] 

    def filter_tag(self, ref):
        find =re.search("\\[\\s*@?tag(.*?)\\s*\\]", ref, re.IGNORECASE)
        ret = None
        if find != None:
            sel = find.group(1)
            alltags = sel.lstrip("~*^=")
            selector = re.sub(alltags, "", sel)
            tagstr = ""
            for tagname in alltags.strip('\'\"').split(" "): 
                tagref = "/tags/tag[name" + selector + tagname.strip(' ') +"]"
                rettag = self._xpath_worker._resolve(tagref)
                if rettag != None:
                    for rt_hnd in rettag.handles():
                        tagstr += rt_hnd + " "
            if len(tagstr) > 0:
                exp = '[usertag-targets' + selector + tagstr.strip(' ') + "]"
                strfind =  find.group().replace("[", "\\[").replace("]", "\\]").replace("@", "\\@")
                strfind = strfind.replace("*", "\\\\*").replace("^", "\\^").replace("~", "\\~").replace("!", "\\!")
                newref = re.sub(strfind, exp, ref)
                ret = self._xpath_worker._resolve(newref)
        return ret

    def post_xpath_resolveSingleObject(self, ret, *args, **kwargs):
        log.debug("worker: pre_xpath_resolveSingleObject")
        ref = args[1]
        self._xpath_worker = args[0]
        fret = self.filter_tag(ref)
        if fret != None:
            return fret.firstNode()

    def post_xpath_resolveObjects(self, ret, *args, **kwargs):
        log.debug("worker: pre_xpath_resolveObjects")
        ref = args[1]
        self._xpath_worker = args[0]
        fret = self.filter_tag(ref)
        if fret != None:
            return fret

    def preprocesstag(self, attributes, backup):
        if type(attributes) is list:
            for child in attributes:
                self.preprocesstag(child, backup)
        elif type(attributes) is dict:
            for key in attributes.keys():
                val = attributes[key]
                if type(val) is list:
                    self.preprocesstag(val, backup)
                elif type(val) is dict:
                    self.preprocesstag(val, backup)
                elif type(val) is str:
                    if re.match(r'tag', key, re.IGNORECASE):
                        retstr = ""
                        for tagname in val.split(" "): 
                            tagref = "/tags/tag[name=" + tagname +"]"
                            ret = self._xpath_worker._resolve(tagref)
                            if ret == None:
                                tparams = {'name': tagname, 'under': 'tags1'}
                                handle = self._rest_worker.create("tag", tparams)
                                self._datamodel_worker.insert(handle, tparams, MapWorker._tags)
                                retstr += handle + " "
                            else:
                                retstr += tagname + " "
                        backup[retstr.strip()] = attributes

    def pre_metamodel_createObject(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_create")
        objects = args[1]
        self._rest_worker = args[0].rest 
        self._datamodel_worker = args[0].datamodel
        if 'project1' in args[0].datamodel.root:
            tags_hnd = args[0].datamodel.root['project1'].children['tags1'].handle
            MapWorker._tags = args[0].datamodel.root['project1'].children['tags1']
        self._xpath_worker = args[0].xpath
        backups = {}
        self.preprocesstag(objects, backups)
        for bk, bk_dict in backups.items():
            bk_dict['usertag-targets'] = bk
            del bk_dict['tag']

    def pre_metamodel_configObject(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_config")
        properties = args[2]
        self._rest_worker = args[0].rest
        self._datamodel_worker = args[0].datamodel
        if 'project1' in args[0].datamodel.root:
            tags_hnd = args[0].datamodel.root['project1'].children['tags1'].handle
            MapWorker._tags = args[0].datamodel.root['project1'].children['tags1']
        self._xpath_worker = args[0].xpath
        self._backups = {}
        self.preprocesstag(properties, self._backups)
        for bk, bk_dict in self._backups.items():
            #bk_dict['usertag-targets'] = bk
            del bk_dict['tag']

    def post_metamodel_configObject(self, ret, *args, **kwargs):
        log.debug("worker: post_metamodel_config")
        for bk, bk_dict in self._backups.items():
            #bk_dict['usertag-targets'] = bk
            del bk_dict['tag']

    def pre_metamodel_performConfig(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_performConfig")
        command = args[1]
        props = args[2]
        self._rest_worker = args[0].rest
        if 'project1' in args[0].datamodel.root:
            tags_hnd = args[0].datamodel.root['project1'].children['tags1'].handle
            MapWorker._tags = args[0].datamodel.root['project1'].children['tags1']
        xpath = args[0].xpath  # for xpath.resolveSingleObject(ref)
 


def process_action():
    def _process(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.debug("enter process_action: %s, %s" % (func.__module__, func.__name__))
            worker = MapWorker(func.__module__, func.__name__)
            worker.pre_process(*args, **kwargs)
            ret = func(*args, **kwargs)
            pret = worker.post_process(ret, *args, **kwargs)
            if pret != None:
                ret = pret
            log.debug("exit process_action: %s, %s" % (func.__module__, func.__name__))
            return ret
        return wrapper
    return _process

