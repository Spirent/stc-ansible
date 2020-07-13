from module_utils.metamodel import MetaModel
from module_utils.tag import TagManager
import pytest


class TestTag:

    def createModel(self):
        self.mm = MetaModel("10.61.67.18")
        result = self.mm.new_session("taguser", "tagsession", ['10.61.67.103', '10.61.67.177'],  ['//10.61.67.103/1/1', '//10.61.67.177/1/1'])
        
        params = {'action': 'create', 'objects': [{'project': [{'port': {'location': '//${chassis[0]}/1/1', 'name': 'Port1'}}, {'port': {'location': '//${chassis[1]}/1/1', 'name': 'Port2'}}]}]}
        self.mm.action(params)

        #params of task: creat device with tag
        params = {'action': 'create', 'under': '/Project', 'count': 3, 'objects': {}}
        params['objects'] = [{'EmulatedDevice': {'AffiliatedPort': "ref:/port[@name='Port1']", 'name': 'BGPRouter', 'tag': 'atag'}}]
        self.mm.action(params)

    def test1(self):
        self.createModel()
        #params of task: creat device with tag
        params = {'action': 'create', 'under': '/Project', 'objects': {}}
        params['objects'] = {'EmulatedDevice': {'AffiliatedPort': "ref:/port[@name='Port1']", 'name': 'BGPRouter', 'tag': 'btag'}}
        tagm = TagManager()
        tagm.update_tag_properties("", params['objects'], self.mm)
        assert 'usertag-targets' in params['objects']['EmulatedDevice']

    def test2(self):
        self.createModel()
        tagm = TagManager()
        #params of task: find device with atag and removing its bgptag
        params = {'action': 'config', 'objects': "/EmulatedDevice[@tag='atag']", "properties": {"tag": "~bgptag &mytag"}}
        ret = tagm.update_tag_references(params['objects'], False, self.mm.xpath)
        assert ret != None and ret.count() > 0
        tagm.update_tag_properties("", params['properties'], self.mm)
        assert 'usertag-targets' in params['properties']

    def test3(self):
        self.createModel()
        params = {'action': 'create', 'under': '/Project', 'objects': {}}
        params['objects'] = [{'EmulatedDevice': {'AffiliatedPort': "ref:/port[@name='Port1']", 'name': 'BGPRouter', 'tag': 'btag'}}]
        self.mm.action(params)
        
        tagm = TagManager()
        #params of task: find device not with atag and configure its bgptag and mytag
        params = {'action': 'config', 'objects': "/EmulatedDevice[@tag!='atag']", "properties": {"tag": "bgptag &mytag"}}
        ret = tagm.update_tag_references(params['objects'], False, self.mm.xpath)
        assert ret != None and ret.count() == 1
        tagm.update_tag_properties("", params['properties'], self.mm)
        assert 'usertag-targets' in params['properties']

    def test4(self):
        self.createModel()
        # intersect tag: 'mytag ctag' and 'ctag'
        params = {'action': 'create', 'under': '/Project', 'objects': {}}
        params['objects'] = [{'EmulatedDevice': {'AffiliatedPort': "ref:/port[@name='Port1']", 'name': 'BGPRouter', 'tag': 'mytag ctag'}}]
        self.mm.action(params)
        
        params = {'action': 'create', 'under': '/Project', 'objects': {}}
        params['objects'] = [{'EmulatedDevice': {'AffiliatedPort': "ref:/port[@name='Port1']", 'name': 'BGPRouter', 'tag': 'ctag'}}]
        self.mm.action(params)

        tagm = TagManager()
        #params of task: find device with ctag and configure its bgptag
        params = {'action': 'config', 'objects': "/EmulatedDevice[@tag*='ctag']", "properties": {"tag": "bgptag"}}
        ret = tagm.update_tag_references(params['objects'], False, self.mm.xpath)
        assert ret != None and ret.count() == 2
        tagm.update_tag_properties("", params['properties'], self.mm)
        assert 'usertag-targets' in params['properties']
