# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-13 14:09:07
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-13 14:11:56

import yaml
import json
import time
from module_utils.metamodel import MetaModel

def test(playbook):


    server = "10.109.122.91"
    pbstart = time.time()
    for task in playbook:

        if "stc" in task:
            print("------------ TASK %s ------------"%task["name"])
            start = time.time()
            model = MetaModel(server)

            # model.verbose()
            # model.rest.verbose()
            # try:
            #     result =model.action(task["stc"])
            # except Exception as error:
            #     print("Oopps... Action error: ",error)
            #     return
            result =model.action(task["stc"])

            elapsed = time.time() - start
            count = task["stc"]["count"] if "count" in task["stc"] else 1
            perobject = int(elapsed*10000/count)/10

            print("task executed in ",int(elapsed*1000),"ms","ms (",perobject,"ms per object)")
            print(json.dumps(result,indent=4))
            # model.dump()

    elapsed = time.time() - pbstart
    perobject = int(elapsed*10000/count)/10
    print("playbook executed in ",int(elapsed*1000),"ms","ms (",perobject,"ms per object)")


with open("playbooks/datamodel-loader.yaml", 'r') as stream:
    try:
        test(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)    

