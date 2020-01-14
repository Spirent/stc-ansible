# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-13 14:09:07
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-14 12:04:40

import yaml
import json
import time
import glob
import sys, os
from module_utils.metamodel import MetaModel


def testPlaybook(playbook, server):

    try:
        with open(playbook, 'r') as stream:
            playbook = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("Invalid YAML:", exc)
        return

    pbstart = time.time()
    for task in playbook:

        if "stc" in task:
            print("\033[93m------------ TASK %s ------------\033[0m" % task["name"])
            start = time.time()
            model = MetaModel(server)

            result = model.action(task["stc"])

            elapsed = time.time() - start
            count = task["stc"]["count"] if "count" in task["stc"] else 1
            perobject = int(elapsed * 10000 / count) / 10

            print("task executed in ", int(elapsed * 1000), "ms", "ms (", perobject, "ms per object)")
            print("Result: \033[96m" + json.dumps(result) + "\033[0m")

    elapsed = time.time() - pbstart
    perobject = int(elapsed * 10000 / count) / 10
    print("playbook executed in ", int(elapsed * 1000), "ms", "ms (", perobject, "ms per object)")


def testPlaybooks(path, server):

    for file in glob.glob(path):

        print("\n\n\n", "=" * 50, "\n\n\n")
        print("Testing playbook %s with server %s" % (file, server))
        testPlaybook(file, server)


if __name__ == "__main__":

    # testPlaybook("playbooks/igmp-network.yaml", os.environ['labserver'])
    testPlaybooks("playbooks/*.yaml", os.environ['labserver'])
