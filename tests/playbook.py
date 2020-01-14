# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-13 14:09:07
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-14 14:09:22

import yaml
import json
import time
import glob
import sys, os
from module_utils.metamodel import MetaModel
from tests.mintaka import MintakaConfig


def testPlaybook(playbook, labServer, ports):

    print("Testing playbook %s with lab server %s and ports %s" % (playbook, labServer, ports))
    try:
        with open(playbook, 'r') as stream:
            playbook = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("Invalid YAML:", exc)
        return

    pbstart = time.time()
    for task in playbook:

        count = 1
        if "stc" in task:
            print("\033[93m------------ TASK %s ------------\033[0m" % task["name"])
            start = time.time()
            model = MetaModel(labServer)

            if task["stc"]["action"] == "session":
                task["stc"]["chassis"] = " ".join(ports)

            result = model.action(task["stc"])

            elapsed = time.time() - start
            count = task["stc"]["count"] if "count" in task["stc"] else 1
            perobject = int(elapsed * 10000 / count) / 10

            print("task executed in ", int(elapsed * 1000), "ms", "ms (", perobject, "ms per object)")
            # print("Result: \033[96m" + json.dumps(result) + "\033[0m")

    elapsed = time.time() - pbstart
    perobject = int(elapsed * 10000 / count) / 10
    print("playbook executed in ", int(elapsed * 1000), "ms", "ms (", perobject, "ms per object)")


def testPlaybooks(path, labServer, ports):

    for file in glob.glob(path):

        print("\n\n\n", "=" * 50, "\n\n\n")
        testPlaybook(file, labServer, ports)


if __name__ == "__main__":

    config = MintakaConfig("cal", "5")
    labServer = config.getLabServer()
    ports = config.getPorts(2)

    testPlaybooks("playbooks/*.yaml", labServer, ports)

    # testPlaybook("playbooks/basic-device.yaml", labServer, ports)
    # testPlaybook("playbooks/igmp-network.yaml", labServer, ports)
