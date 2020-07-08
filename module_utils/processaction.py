
try:
    from module_utils.tag import Tag
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.utils import *
except ImportError:
    from module_utils.tag import Tag
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
                    for key, val in objdict['session'].items():
                        params[key] = val
                    bcreatesession = True
                    break
            if bcreatesession:
                if "objects" in params: 
                    del params['objects'] 
                if "object" in params: 
                    del params['object'] 

    def post_xpath_resolveSingleObject(self, ret, *args, **kwargs):
        log.debug("worker: post_xpath_resolveSingleObject")
        xpath_worker = args[0]
        ref = args[1]
        tag_instance = Tag.create_tag_by_ref(ref)
        if tag_instance != None:
            fret = tag_instance.resolve_by_tag(xpath_worker)
            if fret != None:
                return fret.firstNode()

    def post_xpath_resolveObjects(self, ret, *args, **kwargs):
        log.debug("worker: post_xpath_resolveObjects")
        xpath_worker = args[0]
        ref = args[1]
        tag_instance = Tag.create_tag_by_ref(ref)
        if tag_instance != None:
            fret = tag_instance.resolve_by_tag(xpath_worker)
            if fret != None:
                return fret

    def pre_metamodel_createObject(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_create")
        objects = args[1]
        metamodel = args[0]
        tags_created = {}
        Tag.init_tags_by_attributes(objects, tags_created)

        taghnds  = ""
        for tag_intance, attr_dict in tags_created.items():
            tag_intance.find_or_create_stctag(metamodel)
            taghnds = tag_intance.configure_with_tag(taghnds)
            attr_dict['usertag-targets'] = taghnds
            if 'tag' in attr_dict:
                del attr_dict['tag']

    def pre_metamodel_configObject(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_config")
        root = args[1].handle
        properties = args[2]
        metamodel = args[0]
        tags_created = {}
        Tag.init_tags_by_attributes(properties, tags_created)

        taghnds = metamodel.rest.get(root, ["usertag-targets"])
        for tag_intance, attr_dict in tags_created.items():
            tag_intance.find_or_create_stctag(metamodel)
            taghnds = tag_intance.configure_with_tag(taghnds)
            attr_dict['usertag-targets'] = taghnds
            if 'tag' in attr_dict:
                del attr_dict['tag']

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

