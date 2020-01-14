# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-13 14:02:28
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-13 14:12:10


class ObjectTree:

    def __init__(self, objects):
        self.objects = []
        self.create(objects, "", {}, "", {})
        self.objects.reverse()

    def create(self, attributes, parent, properties, under, children):

        # print(">>>>",type(attributes),parent,":",attributes)
        if type(attributes) is list:

            # Expect that the sub-childs are dictionnaries
            for child in attributes:
                if not type(child) is dict:
                    raise Exception("Invalid attribute type %s for %s under %s" % (type(child), child, parent))

                for key in child.keys():
                    subchildren = {}
                    subproperties = {}
                    nodeid = parent + "." + key if parent != "" else key
                    self.create(child[key], "", subproperties, nodeid, subchildren)
                    obj = {"type": key, "props": subproperties, "children": subchildren}
                    if under != "":
                        obj["under"] = under
                    self.objects.append(obj)

        elif type(attributes) is dict:

            for key in attributes.keys():
                val = attributes[key]
                nodeid = parent + "." + key if parent != "" else key

                if type(val) is list:
                    children[nodeid] = val
                    self.create(val, nodeid, properties, key, children)

                elif type(val) is dict:
                    if parent != "":
                        children[parent][key] = None
                    children[nodeid] = val
                    self.create(val, nodeid, properties, under + "." + key, children)

                elif type(val) is str:
                    properties[nodeid] = val

                elif type(val) is int:
                    properties[nodeid] = val

                elif type(val) is bool:
                    properties[nodeid] = val

                else:
                    print("[objtree] Unknown type %s [%s:%s]" % (type(val), key, val))
                    exit()

        else:

            raise Exception("Invalid attribute %s type %s" % (attributes, type(attributes)))
