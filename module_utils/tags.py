# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-07-13 16:58:59

try:
    from ansible.module_utils.logger import Logger

except ImportError:
    from module_utils.logger import Logger

log = Logger("TagManager")


class TagManager:

    def __init__(self, rstHdl):
        self.rest = rstHdl
        self.tags = {}

    def getPoppedTags(self, objects):
        log.info("POPPING tags From object: %s" % (str(objects)))
        val = objects.get('tag')
        if val == None:
            log.info("No tags contained in objects!")
            return {}

        else:
            objects.pop("tag")
            return {'tag': val}

    def handleTags(self, objects, index=0):
        log.info("HANDLE tags From object: %s, index: %d" % (str(objects), index))
        val = objects.get('tag')
        if val == None:
            log.info("No tags contained in objects!")
            return

        val = val.replace("$item", str(index))

        objects.pop("tag")
        objects["usertag-targets"] = self.getTagsHandle(val)

        return

    def initTags(self):

        if len(self.tags) != 0:
            log.info("Tags have been updated!")
            return

        children = self.rest.children("tags1")
        for handle in children:
            tagProps = self.rest.get(handle)
            self.tags[tagProps['Name']] = handle

        log.info("The existing Tags: %s" % str(self.tags))
        return

    def getTagByName(self, tagName):
        handle = self.tags.get(tagName)
        if handle != None:
            return handle

        #Create tags for tagName
        props = {'Name': tagName, 'under': 'tags1'}
        handle = self.rest.create("tag", props)

        self.tags[tagName] = handle
        log.info("After creating, Tags: %s" % str(self.tags))
        return handle

    def getTagsHandle(self, tagNames):
        tagList = tagNames.split(' ')
        log.info("Handle Tags in List: %s" % str(tagList))
        self.initTags()
        handles = []
        for tagName in tagList:
            handles.append(self.getTagByName(tagName))

        return " ".join(handles)

