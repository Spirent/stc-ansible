# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-13 14:09:07
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-02-06 12:35:40

import yaml
import json
import time
import glob
import shutil
import sys, os
import re
from module_utils.utils import *
from module_utils.metamodel import MetaModel
from tests.mintaka import MintakaConfig


class PlaybookEmulator:

    def __init__(self, labServer, chassis=[], ports=[], names=[]):

        if labServer[0] == '@':
            config = MintakaConfig(labServer[1:], "5")
            labServer = config.getLabServer()
            chassis = config.getPorts(2)
            ports = ["//" + ip + "/1/1" for ip in chassis]

        self.labServer = labServer
        self.chassis = chassis
        self.ports = ports
        self.names = names

    def play(self, playbook):

        print("Testing playbook %s with lab server %s and chassis %s" % (playbook, self.labServer, self.chassis))
        try:
            with open(playbook, 'r') as stream:
                playbook = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Invalid YAML:", exc)
            return

        if len(playbook) > 0 and "tasks" in playbook[0]:
            playbook = playbook[0]["tasks"]

        pbstart = time.time()
        for task in playbook:

            if not "name" in task:
                task["name"] = "???"

            count = 1
            if "pause" in task:
                print("\033[93m------------ PAUSING ------------\033[0m")
                if "pause" in task:
                    if "seconds" in task["pause"]:
                        print("Waiting for %s seconds" % task["pause"]["seconds"])
                        time.sleep(int(task["pause"]["seconds"]))
                    elif "minutes" in task["pause"]:
                        print("Waiting for %s minutes" % task["pause"]["minutes"])
                        time.sleep(int(task["pause"]["minutes"]) * 60)
                    else:
                        print("Sorry, I do not understand this task... %s" % task)
                else:
                    print("Sorry, I do not understand this task... %s" % task)

            elif "stc" in task:
                print("\033[93m------------ TASK %s ------------\033[0m" % task["name"])
                start = time.time()
                model = MetaModel(self.labServer)

                if task["stc"]["action"] == "session":
                    if len(self.chassis) > 0:
                        print("[emulator] Overwritting Chassis with %s" % self.chassis)
                        task["stc"]["chassis"] = " ".join(self.chassis)

                    print("**** ports:", task["stc"]["ports"])
                    mgPort = re.search(r'\{\{(\s*)hostvars\[inventory_hostname\]\.ports(\s*)\}\}', task["stc"]["ports"])
                    print("**** names:", task["stc"]["names"])
                    if len(self.ports) > 0 and mgPort:
                        print("[emulator] Overwritting Ports with %s" % self.ports)
                        task["stc"]["ports"] = " ".join(self.ports)

                    mgName = re.search(r'\{\{(\s*)hostvars\[inventory_hostname\]\.names(\s*)\}\}', task["stc"]["names"])
                    if len(self.names) > 0 and mgName:
                        print("[emulator] Overwritting Names with %s" % self.names)
                        task["stc"]["names"] = " ".join(self.names)

                if "dest" in task["stc"]:
                    task["stc"]["dest"] = task["stc"]["dest"].replace("{{ tempfolder.path }}", "/tmp")

                if "datamodel" in task["stc"] and "action" in task["stc"] :
                    task["stc"]["datamodel"] = task["stc"]["datamodel"].replace("{{ tempfolder.path }}", "asset")
                    
                result = model.action(task["stc"])

                if result.isError():
                    print(Color.red("-" * 80))
                    print(Color.red(" *** error *** ") + ": " + result.err)
                    print(Color.red("-" * 80))
                    print("aborting...")
                    exit()
                else:
                    result = result.val

                elapsed = time.time() - start
                count = task["stc"]["count"] if "count" in task["stc"] else 1
                perobject = int(elapsed * 10000 / count) / 10

                print("task executed in ", int(elapsed * 1000), "ms", "ms (", perobject, "ms per object)")

                if "register" in task:
                    if type(result) is str:
                        print("Result: \033[96m" + result + "\033[0m")
                    else:
                        print("Result: \033[96m" + json.dumps(result, indent=4) + "\033[0m")

            elif "copy" in task:
                src = task["copy"]["src"].replace("{{ tempfolder.path }}", "asset")
                dst = task["copy"]["dest"].replace("{{ tempfolder.path }}", "asset")
                if src != dst:
                    shutil.copyfile(src, dst)

            elif not "debug" in task:
                print("\033[93m------------ UNKNOWN TASK ------------\033[0m")
                print("Sorry, I do not understand this task... %s" % task)

        elapsed = time.time() - pbstart
        perobject = int(elapsed * 10000 / count) / 10
        print("playbook executed in ", int(elapsed * 1000), "ms", "ms (", perobject, "ms per object)")


if __name__ == "__main__":

    emulator = PlaybookEmulator("@bdc")

    # emulator.play("./playbooks/bgp-traffic.yaml")

    for file in glob.glob("./playbooks/*.yaml"):
        print("\n\n%s %s %s\n\n" % (Color.blue("=" * 60), Color.bold(file), Color.blue("=" * 60)))
        emulator.play(file)
