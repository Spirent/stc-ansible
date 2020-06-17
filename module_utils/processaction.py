
try:
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.utils import *
except ImportError:
    from module_utils.logger import Logger
    from module_utils.utils import * 


import functools

log = Logger("processaction")

class Worker:
    def __init__(self, method_name):
        self._method = method_name
    
    def pre_process(self, *args, **kwargs):
        pre_func = getattr(self, "pre_"+self._method, None)
        if pre_func != None:
            return pre_func(*args, **kwargs)
        log.debug("worker: without pre_%s" % self._method)

    def post_process(self, ret, *args, **kwargs):
        post_func = getattr(self, "post_"+self._method, None)
        if post_func != None:
            return post_func(ret, *args, **kwargs)
        log.debug("worker: without post_%s" % self._method)

    def pre_action(self, *args, **kwargs):
        params = args[1]
        action = params["action"]
        if action == "create":
            objects = params["objects"] if "objects" in params else None
            if objects == None and "object" in params:
                objects = params["object"]
            for objdict in objects:
                if 'session' in objdict:
                    params['action'] = 'session'
                    params['user'] = objdict['session']['user']
                    params['name'] = objdict['session']['name']
                    params['chassis'] = objdict['session']['chassis']
            if "objects" in params: 
                del params['objects'] 
            if "object" in params: 
                del params['object'] 
        log.debug("worker: pre_action")

    def pre_create(self, *args, **kwargs):
        objects = args[1]
        if 'under' in kwargs:
            under = kwargs['under']
        if 'count' in kwargs:
            count = kwargs['count']
        log.debug("worker: pre_create")

    def post_create(self, ret, *args, **kwargs):
        #ret="myret"  //dummy code
        log.debug("worker: post_create")

    def pre_config(self, *args, **kwargs):
        properties = args[1]
        if 'objref' in kwargs:
            objref = kwargs['objref']
        if 'count' in kwargs:
            count = kwargs['count']
        log.debug("worker: pre_create")

    def post_config(self, ret, *args, **kwargs):
        log.debug("worker: post_create")

    def pre_performConfig(self, *args, **kwargs):
        command = args[1]
        props = args[2]
        log.debug("worker: pre_performConfig")
     
    def post_performConfig(self, ret, *args, **kwargs):
        #ret="myret"  //dummy code
        log.debug("worker: post_performConfig")


def process_action():
    def _process(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.debug("enter process_action: %s" % func.__name__)
            worker = Worker(func.__name__)
            worker.pre_process(*args, **kwargs)
            r = func(*args, **kwargs)
            ret = worker.post_process(r, *args, **kwargs)
            log.debug("exit process_action: %s" % func.__name__)
            return ret
        return wrapper
    return _process