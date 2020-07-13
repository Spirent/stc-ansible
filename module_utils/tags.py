# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-07-13 16:58:59

try:
    from ansible.module_utils.xpath import NodeSelector
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.utils import *
except ImportError:
    import sys
    from os.path import os, abspath, dirname, join
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.normpath(os.path.join(path, '../')))
    from module_utils.logger import Logger
    from module_utils.xpath import NodeSelector

import re

log = Logger("tag")


class TagManager:

    def __init__(self, mm):
        self.metamodel = mm
        self.tags = None

    def update(self, objects):

        tags_created = {}
        self._init_tags_by_attributes(objects, tags_created)
        return tags_created

    def _init_tags_by_attributes(self, attributes, tags_created={}):

        if type(attributes) is list:
            for child in attributes:
                self._init_tags_by_attributes(child, tags_created)

        elif type(attributes) is dict:

            keys = attributes.keys()
            if "tag" in keys:
                handles = []
                for tagname in attributes["tag"].split(" "):
                    handle = self._create_tag_by_name(tagname)
                    handles.append(handle)
                    tags_created[handle] = attributes
                attributes.pop("tag")
                attributes["usertag-targets"] = " ".join(handles)
                return

            for key in attributes.keys():

                val = attributes[key]
                if type(val) is list:
                    self._init_tags_by_attributes(val, tags_created)

                elif type(val) is dict:
                    self._init_tags_by_attributes(val, tags_created)

    def _init_datamodel_tags(self):

        if self.tags == None:
            tags = self.metamodel.rest.get("tags1")
            if len(tags["children"]):
                self.tags = dict((handle, self.metamodel.rest.get(handle)) for handle in tags["children"].split(" "))
            else:
                self.tags = []

    def _create_tag_by_name(self, tagname):

        self._init_datamodel_tags()
        for handle, tag in self.tags.items():
            if ("Name" in tag) and tag["Name"] == tagname:
                return handle
            if ("name" in tag) and tag["name"] == tagname:
                return handle

        props = {'Name': tagname, 'under': 'tags1'}
        handle = self.metamodel.rest.create("tag", props)
        self.tags[handle] = props
        return handle
