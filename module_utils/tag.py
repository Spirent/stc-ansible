
try:
    from ansible.module_utils.logger import Logger
    from ansible.module_utils.utils import *
except ImportError:
    import sys
    from os.path import os, abspath, dirname, join
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.normpath(os.path.join(path, '../')))
    from module_utils.logger import Logger

import re

log = Logger("tag")

class TagManager:
    def update_tag_references(self, ref, single,  xpath_worker):
        tag_instance = self.create_tag_by_ref(ref)
        if tag_instance != None:
            fret = tag_instance.resolve_by_tag(xpath_worker)
            if fret != None:
                if single:
                    return fret.firstNode()
                else:
                    return fret

    def update_tag_properties(self, taghnds, objects, metamodel):
        tags_created = {}
        self.init_tags_by_attributes(objects, tags_created)
        taghnds  = ""
        for tag_intance, attr_dict in tags_created.items():
            tag_intance.find_or_create_stctag(metamodel)
            taghnds = tag_intance.configure_with_tag(taghnds)
            attr_dict['usertag-targets'] = taghnds
            if 'tag' in attr_dict:
                del attr_dict['tag']

    def create_tag_by_ref(self, ref_exp, tagname=""):
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
        elif ref_exp == "":
            if re.match(r'^\~', tagname) != None:
                return TagOnRemoved(ref_exp, tagname)
            else:
                return TagOnAdded(ref_exp, tagname)
        return None
   
    def init_tags_by_attributes(self, attributes, tags_created={}):
        if type(attributes) is list:
            for child in attributes:
                self.init_tags_by_attributes(child, tags_created)
        elif type(attributes) is dict:
            for key in attributes.keys():
                val = attributes[key]
                if type(val) is list:
                    self.init_tags_by_attributes(val, tags_created)
                elif type(val) is dict:
                    self.init_tags_by_attributes(val, tags_created)
                elif type(val) is str:
                    if re.match(r'tag', key, re.IGNORECASE):
                        for tagname in val.split(" "): 
                            tagref = "/tags/tag[name=" + tagname +"]"
                            tag_intance = self.create_tag_by_ref("", tagname)
                            tags_created[tag_intance] = attributes

class Tag:
    _meta_tags = None
    def __init__(self, ref_exp="", tagname=""):
        self._exp = ref_exp
        if ref_exp != "":
            find =re.search("\\[\\s*@?tag(.*?)\\s*\\]", ref_exp, re.IGNORECASE)
            if find != None and tagname == "":
                sel = find.group(1).strip("\'\"")
                self._tagname = re.sub(r'\^=|\*=|\~=|\!=|=|\'', '', sel)
        else:
            self._tagname = re.sub(r'\&|\~|\'', '', tagname)
    
    def find_or_create_stctag(self, metamodel_inst):
        Tag._meta_tags = metamodel_inst.datamodel.root['project1'].children['tags1']
        return None

    def configure_with_tag(self, tag_objs):
        pass


class TagSelector(Tag):
    def __init__(self, ref_exp, tagname):
        Tag.__init__(self, ref_exp, tagname)
        self._selector = ""

    def resolve_by_tag(self, xpath_inst):
        pass

class TagOnEqual(TagSelector):
    def __init__(self, ref_exp, tagname):
        TagSelector.__init__(self, ref_exp, tagname)
        self._selector = "="

    def resolve_by_tag(self, xpath_inst):
        ret = None
        if self._tagname != None and self._tagname != "":
            find =re.search("\\[\\s*@?tag(.*?)\\s*\\]", self._exp, re.IGNORECASE)
            for tag in self._tagname.strip('\'\"').split(" "): 
                tagref = "/tags/tag[name" + self._selector + tag.strip(' ') +"]"
                rettag = xpath_inst._resolve(tagref)
                if rettag != None:
                    for rt_hnd in rettag.handles():
                        exp = '[usertag-targets*=' + rt_hnd  + "]"
                        strfind =  find.group().replace("[", "\\[").replace("]", "\\]").replace("@", "\\@")
                        strfind = strfind.replace("*", "\\*").replace("^", "\\^").replace("~", "\\~").replace("!", "\\!")
                        newref = re.sub(strfind, exp, self._exp)
                        myret = xpath_inst._resolve(newref)
                        if ret == None:
                            ret = myret
                        elif ret != None and ret.isDifferent(myret):
                            return None
        return ret

class TagOnContains(TagSelector):
    def __init__(self, ref_exp, tagname):
        TagSelector.__init__(self, ref_exp, tagname)
        self._selector = "*="

    def resolve_by_tag(self, xpath_inst):
        ret = None
        if self._tagname != None and self._tagname != "":
            find =re.search("\\[\\s*@?tag(.*?)\\s*\\]", self._exp, re.IGNORECASE)
            for tag in self._tagname.strip('\'\"').split(" "): 
                tagref = "/tags/tag[name" + self._selector + tag.strip(' ') +"]"
                rettag = xpath_inst._resolve(tagref)
                if rettag != None:
                    for rt_hnd in rettag.handles():
                        exp = '[usertag-targets*=' + rt_hnd  + "]"
                        strfind =  find.group().replace("[", "\\[").replace("]", "\\]").replace("@", "\\@")
                        strfind = strfind.replace("*", "\\*").replace("^", "\\^").replace("~", "\\~").replace("!", "\\!")
                        newref = re.sub(strfind, exp, self._exp)
                        myret = xpath_inst._resolve(newref)
                        if ret == None:
                            ret = myret
                        elif ret != None and ret.isDifferent(myret):
                            ret.extend(myret)
        return ret


class TagOnDifferent(TagSelector):
    def __init__(self, ref_exp, tagname):
        TagSelector.__init__(self, ref_exp, tagname)
        self._selector = "!="

    def resolve_by_tag(self, xpath_inst):
        ret = None
        if self._tagname != None:
            tagstr = ""
            for tag in self._tagname.strip('\'\"').split(" "): 
                tagref = "/tags/tag[name=" + tag.strip(' ') +"]"
                rettag = xpath_inst._resolve(tagref)
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
                ret = xpath_inst._resolve(newref)
        return ret


class TagOnStartswith(TagSelector):
    def __init__(self, ref_exp, tagname):
        TagSelector.__init__(self, ref_exp, tagname)
        self._selector = "^="

    def resolve_by_tag(self, xpath_inst):
        pass


class TagConfig(Tag):
    def __init__(self, ref_exp, tagname):
        Tag.__init__(self, ref_exp, tagname)
        self._selector = ""

    def find_or_create_stctag(self, metamodel_inst):
        return Tag.find_or_create_stctag(self, metamodel_inst)

    def configure_with_tag(self, tag_objs):
        pass

class TagOnAdded(TagConfig):
    def __init__(self, ref_exp, tagname):
        TagConfig.__init__(self, ref_exp, tagname)
        self._selector = "&"

    def find_or_create_stctag(self, metamodel_inst):
        TagConfig.find_or_create_stctag(self, metamodel_inst)
        self._handle = None
        if self._tagname != None and self._tagname != "":
            ftag = self._tagname
            tagref = "/tags/tag[name=" + ftag +"]"
            ret = metamodel_inst.xpath._resolve(tagref)
            if ret == None:
                tparams = {'name': ftag, 'under': 'tags1'}
                handle = metamodel_inst.rest.create("tag", tparams)
                metamodel_inst.datamodel.insert(handle, tparams, Tag._meta_tags)
                self._handle = handle
            else:
                self._handle = ret.firstNode().handle
        return self._handle

    def configure_with_tag(self, tag_objs):
        if tag_objs == None or tag_objs == "":
            return self._handle
        new_taghnds = tag_objs
        if self._handle != None and self._handle != "":
            if re.search(self._handle, tag_objs) == None:
                new_taghnds = new_taghnds + " " + self._handle
        return new_taghnds

class TagOnRemoved(TagConfig):
    def __init__(self, ref_exp, tagname):
        TagConfig.__init__(self, ref_exp, tagname)
        self._selector = "~"

    def find_or_create_stctag(self, metamodel_inst):
        TagConfig.find_or_create_stctag(self, metamodel_inst)
        self._handle = None
        if self._tagname != None and self._tagname != "":
            ftag = self._tagname
            tagref = "/tags/tag[name=" + ftag +"]"
            ret = metamodel_inst.xpath._resolve(tagref)
            if ret != None:
                self._handle = ret.firstNode().handle
        return self._handle

    def configure_with_tag(self, tag_objs):
        if tag_objs == None or tag_objs == "":
            return ""
        new_taghnds = tag_objs
        new_taghnds = re.sub(self._handle +" ", '', new_taghnds)
        new_taghnds = re.sub(" "+self._handle, '', new_taghnds)
        new_taghnds = re.sub(self._handle, '', new_taghnds)
        return new_taghnds

#
# Some test code that run Tag
#
if __name__ == '__main__':
    try:
        from ansible.module_utils.metamodel import MetaModel
    except ImportError:
        from module_utils.metamodel import MetaModel

    mm = MetaModel("10.61.67.215")
    result = mm.new_session("taguser", "tagsession", ['10.61.67.103', '10.61.67.177'],  ['//10.61.67.103/1/1', '//10.61.67.177/1/1'], True, False)
    
    params = {'action': 'create', 'objects': [{'project': [{'port': {'location': '//${chassis[0]}/1/1', 'name': 'Port1'}}, {'port': {'location': '//${chassis[1]}/1/1', 'name': 'Port2'}}]}]}
    mm.action(params)

    #params of task: creat device with tag
    params = {'action': 'create', 'under': '/Project', 'objects': {}}
    params['objects'] = [{'EmulatedDevice': {'AffiliatedPort': "ref:/port[@name='Port1']", 'name': 'BGPRouter', 'tag': 'atag'}}]
    tags_created = {}
    tagm = TagManager()
    tagm.update_tag_properties("", params['objects'], mm)

    #params of task: find device with tag and configure its tag
    params = {'action': 'config', 'objects': "/EmulatedDevice[@tag='atag']", "properties": {"tag": "~bgptag &mytag"}}
    tagm.update_tag_references(params['objects'], True, mm.xpath)
    tagm.update_tag_properties("", params['properties'], mm)
