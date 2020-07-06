
try:
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.utils import *
    from ansible.module_utils.metamodel import MetaModel
except ImportError:
    import sys
    from os.path import os, abspath, dirname, join
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.normpath(os.path.join(path, '../')))
    from module_utils.logger import Logger
    from module_utils.metamodel import MetaModel

import re

log = Logger("tag")

CREATE = 1
REMOVE = 2

class TagManager:
    _meta_tags = None
    def __init__(self, ref_exp="", tagname=""):
        self._exp = ref_exp
        self._tagname = tagname
        if ref_exp != "":
            find =re.search("\\[\\s*@?tag(.*?)\\s*\\]", ref_exp, re.IGNORECASE)
            if find != None:
                sel = find.group(1).strip("\'\"")
                self._tagname = re.sub(r'\^=|\*=|\~=|\!=|=|\'', '', sel)
        self._state = CREATE
        self._metamodel = MetaModel._instance
        TagManager._meta_tags = MetaModel._instance.datamodel.root['project1'].children['tags1']
    
    def init_tag_by_attributes(self, attributes, tag_bk):
        if type(attributes) is list:
            for child in attributes:
                self.init_tag_by_attributes(child, tag_bk)
        elif type(attributes) is dict:
            for key in attributes.keys():
                val = attributes[key]
                if type(val) is list:
                    self.init_tag_by_attributes(val, tag_bk)
                elif type(val) is dict:
                    self.init_tag_by_attributes(val, tag_bk)
                elif type(val) is str:
                    if re.match(r'tag', key, re.IGNORECASE):
                        for tagname in val.split(" "): 
                            tagref = "/tags/tag[name=" + tagname +"]"
                            tag_intance = self.new_tag_by_ref(tagref, tagname)
                            tag_bk[tag_intance] = attributes

    def new_tag_by_ref(self, ref_exp, tagname=""):
        find =re.search("\\[\\s*@?tag(.*?)\\s*\\]", ref_exp, re.IGNORECASE)
        if find == None:
            find = re.search("\\/tags\\/tag\\[\\s*@?name(.*?)\\s*\\]", ref_exp, re.IGNORECASE)
        if find != None:
            sel = find.group(1)
            if re.match(r'^=', sel) != None:
                return TagOnEqual(ref_exp, tagname)
            elif re.match(r'^\*=', sel) != None:
                return TagOnContains(ref_exp, tagname)
            elif re.match(r'^~=', sel) != None:
                return TagOnContains(ref_exp, tagname)
            elif re.match(r'^\!=', sel) != None:
                return TagOnDifferent(ref_exp, tagname)
            elif re.match(r'^\^=', sel) != None:
                return TagOnStartswith(ref_exp, tagname)

    def find_or_create_stctag(self):
        if self._exp != None and self._exp != "":
            ftag = self._tagname
            bRemove = re.match(r'^~', ftag)
            if bRemove != None:
                ftag = re.sub(r'~', '', ftag)
                self._state = REMOVE
            bAdd = re.match(r'^&', ftag)
            if bAdd != None:
                ftag = re.sub(r'&', '', ftag)
                self._state = CREATE
            tagref = "/tags/tag[name=" + ftag +"]"
            ret = self._metamodel.xpath._resolve(tagref)
            if ret == None:
                if  bRemove == None:
                    tparams = {'name': ftag, 'under': 'tags1'}
                    handle = self._metamodel.rest.create("tag", tparams)
                    self._metamodel.datamodel.insert(handle, tparams, TagManager._meta_tags)
                    return handle
            else:
                return ret.firstNode().handle

    def resolve_by_tag(self):
        pass

    def configure_with_tag(self, objects):
        pass
    

class TagOnEqual(TagManager):
    def __init__(self, ref_exp, tagname):
        TagManager.__init__(self, ref_exp, tagname)
        self._selector = "="

    def resolve_by_tag(self):
        ret = None
        if self._tagname != None:
            tagstr = ""
            for tag in self._tagname.strip('\'\"').split(" "): 
                tagref = "/tags/tag[name" + self._selector + tag.strip(' ') +"]"
                rettag = self._metamodel.xpath._resolve(tagref)
                if rettag != None:
                    for rt_hnd in rettag.handles():
                        tagstr += rt_hnd + " "
            if len(tagstr) > 0:
                find =re.search("\\[\\s*@?tag(.*?)\\s*\\]", self._exp, re.IGNORECASE)
                if find != None:
                    exp = '[usertag-targets' + self._selector + tagstr.strip(' ') + "]"
                    strfind =  find.group().replace("[", "\\[").replace("]", "\\]").replace("@", "\\@")
                    strfind = strfind.replace("*", "\\*").replace("^", "\\^").replace("~", "\\~").replace("!", "\\!")
                    newref = re.sub(strfind, exp, self._exp)
                ret = self._metamodel.xpath._resolve(newref)
        return ret

    def configure_with_tag(self, objects):
        if objects != None and objects != "" and self._tagname != None:
            tagstr = ""
            for tag in self._tagname.strip('\'\"').split(" "): 
                tagref = "/tags/tag[name" + self._selector + tag.strip(' ') +"]"
                rettag = self._metamodel.xpath._resolve(tagref)
                if rettag != None:
                    for rt_hnd in rettag.handles():
                        tagstr += rt_hnd + " "
            if len(tagstr) > 0:
                newtagstr = tagstr
                for object in objects:
                    tag_hnds = self._metamodel.rest.get(object, 'usertag-targets')
                    newtagstr += tag_hnds
                    self._metamodel.rest.config(object, 'usertag-targets '+ newtagstr.strip(' '))

class TagOnContains(TagManager):
    def __init__(self, ref_exp, tagname):
        TagManager.__init__(self, ref_exp, tagname)
        self._selector = "*="

    def resolve_by_tag(self):
        pass
    def configure_with_tag(self, objects):
        pass

class TagOnDifferent(TagManager):
    def __init__(self, ref_exp, tagname):
        TagManager.__init__(self, ref_exp, tagname)
        self._selector = "!="

    def resolve_by_tag(self):
        pass

    def configure_with_tag(self, objects):
        pass

class TagOnStartswith(TagManager):
    def __init__(self, ref_exp, tagname):
        TagManager.__init__(self, ref_exp, tagname)
        self._selector = "^="

    def resolve_by_tag(self):
        pass

    def configure_with_tag(self, objects):
        pass

#
# Some test code that run Tag
#
if __name__ == '__main__':
    mm = MetaModel("10.61.67.215")
    result = mm.new_session("taguser", "tagsession", ['10.61.67.103', '10.61.67.177'],  ['//10.61.67.103/1/1', '//10.61.67.177/1/1'], True, False)
    
    params = {'action': 'create', 'objects': [{'project': [{'port': {'location': '//${chassis[0]}/1/1', 'name': 'Port1'}}, {'port': {'location': '//${chassis[1]}/1/1', 'name': 'Port2'}}]}]}
    mm.action(params)

    #params of task: creat device with tag
    params = {'action': 'create', 'under': '/Project', 'objects': {}}
    params['objects'] = [{'EmulatedDevice': {'AffiliatedPort': "ref:/port[@name='Port1']", 'name': 'BGPRouter', 'tag': 'atag'}}]
    tagm = TagManager()
    tag_backup = {}
    tagm.init_tag_by_attributes(params['objects'], tag_backup)
    for tag_intance, attr in tag_backup.items():
        tag_stchnd = tag_intance.find_or_create_stctag()

    #params of task: find device with tag and configure its tag
    params = {'action': 'config', 'objects': "/EmulatedDevice[@tag='atag']", "properties": {"tag": "~bgptag &mytag"}}
    tag_instance = tagm.new_tag_by_ref(params['objects'])
    devhnd = tag_instance.resolve_by_tag()
    tag_instance.configure_with_tag(devhnd)
