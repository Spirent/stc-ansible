
try:
    from module_utils.tag import TagManager
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.utils import *
except ImportError:
    from module_utils.tag import TagManager
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
        tagm = TagManager()
        return tagm.update_tag_references(ref, True, xpath_worker)

    def post_xpath_resolveObjects(self, ret, *args, **kwargs):
        log.debug("worker: post_xpath_resolveObjects")
        xpath_worker = args[0]
        ref = args[1]
        tagm = TagManager()
        return tagm.update_tag_references(ref, False, xpath_worker)

    def pre_metamodel_createObject(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_createObject")
        objects = args[1]
        metamodel = args[0]
        tagm = TagManager()
        tagm.update_tag_properties("", objects, metamodel)

    def pre_metamodel_configObject(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_configObject")
        root = args[1].handle
        properties = args[2]
        metamodel = args[0]
        taghnds = metamodel.rest.get(root, ["usertag-targets"])
        tagm = TagManager()
        tagm.update_tag_properties(taghnds, properties, metamodel)

    def pre_metamodel_perform(self, *args, **kwargs):
        log.debug("worker: pre_metamodel_perform")
        properties = args[2]
        metamodel = args[0]
        tagm = TagManager()
        tagm.update_tag_properties("", properties, metamodel)

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

