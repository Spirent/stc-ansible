# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-13 14:09:07
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-19 23:36:10

import yaml
import json
import time
import glob
import shutil
import sys, os
from module_utils.utils import *
from module_utils.metamodel import MetaModel
from tests.mintaka import MintakaConfig


class PlaybookEmulator:

    def __init__(self, labServer, chassis=[]):

        if labServer[0] == '@':
            config = MintakaConfig(labServer[1:], "5")
            labServer = config.getLabServer()
            chassis = config.getPorts(2)

        self.labServer = labServer
        self.chassis = chassis

    def play(self, playbook):

        print("Testing playbook %s with lab server %s and chassis %s" % (playbook, self.labServer, self.chassis))
        try:
            with open(playbook, 'r') as stream:
                playbook = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Invalid YAML:", exc)
            return

        pbstart = time.time()
        for task in playbook:

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

                if task["stc"]["action"] == "session" and len(self.chassis) > 0:
                    print("[emulator] Overwritting Chassis with %s" % self.chassis)
                    task["stc"]["chassis"] = " ".join(self.chassis)

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
                    print("Result: \033[96m" + json.dumps(result, indent=4) + "\033[0m")

            elif "copy" in task:
                shutil.copyfile(task["copy"]["src"], task["copy"]["dest"])

            elif not "debug" in task:
                print("\033[93m------------ UNKNOWN TASK ------------\033[0m")
                print("Sorry, I do not understand this task... %s" % task)

        elapsed = time.time() - pbstart
        perobject = int(elapsed * 10000 / count) / 10
        print("playbook executed in ", int(elapsed * 1000), "ms", "ms (", perobject, "ms per object)")


def testPlaybooks(path, labServer, ports):

    for file in glob.glob(path):

        print("\n\n\n", "=" * 50, "\n\n\n")
        testPlaybook(file, labServer, ports)


if __name__ == "__main__":

    emulator = PlaybookEmulator("@bdc")
    for file in glob.glob("./playbooks/*.yaml"):
        print("\n\n%s %s %s\n\n" % (Color.blue("=" * 60), Color.bold(file), Color.blue("=" * 60)))
        emulator.play(file)
