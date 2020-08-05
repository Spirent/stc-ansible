
from module_utils.tags import TagManager

import pytest


class RestMock:

    def __init__(self):
        self.count = 10

    def create(self, handle, props):

        self.count = self.count + 1
        return handle + "-" + str(self.count)

    def children(self, handle):
        return ['tag1', 'tag2']

    def get(self, handle, props=""):

        if handle == "tag1":
            return {
                "Active": "true",
                "parent": "tags1",
                "defaulttag-Sources": "tags1",
                "Name": "Router" }
        if handle == "tag2":
            return {
                "Active": "true",
                "parent": "tags1",
                "defaulttag-Sources": "tags1",
                "Name": "Client" }


class TestTags:

    def createTagManager(self):
        return TagManager(RestMock())

    def test1a(self):
        tM = self.createTagManager()

        params = {'under': 'project1',
                  'location': '//10.61.67.78/1/1',
                  'name': 'Port1',
                  'tag': 'Router portdhcp'}

        tM.handleTags(params)
        val = params.get('tag')

        assert val == None
        assert params["usertag-targets"] == "tag1 tag-11"

    def test2a(self):
        tM = self.createTagManager()

        params = {'ParentList': 'ref:/project',
                  'CreateCount': 2,
                  'DeviceCount': 5,
                  'Port': "ref:/port[@name='Port1']",
                  'IfStack': 'Ipv4If PppIf PppoeIf EthIIIf',
                  'IfCount': '1 1 1 1',
                  'name': 'dev-$item',
                  'tag': 'devtagzyf devtag-0'}

        tM.handleTags(params)
        val = params.get('tag')

        assert val == None
        assert params["usertag-targets"] == "tag-11 tag-12"

    def test3a(self):
        tM = self.createTagManager()

        params = {'under': 'project1',
                  'tag': 'Client traff-0',
                  'EnableStreamOnlyGeneration': True,
                  'TrafficPattern': 'MESH',
                  'SrcBinding-targets': 'ipv4if1',
                  'DstBinding-targets': 'ipv4if2',
                  'AffiliationStreamBlockLoadProfile.Load': 100}

        tM.handleTags(params)
        val = params.get('tag')

        assert val == None
        assert params["usertag-targets"] == "tag2 tag-11"

    def test4a(self):
        tM = self.createTagManager()

        params = {'under': 'project1',
                  'location': '//10.61.67.78/1/1',
                  'name': 'Port1'}

        tM.handleTags(params)

        assert params == params


    def test1b(self):
        tM = self.createTagManager()

        params = {'under': 'project1',
                  'tag': 'Client traff-$item',
                  'EnableStreamOnlyGeneration': True,
                  'TrafficPattern': 'MESH',
                  'SrcBinding-targets': 'ipv4if1',
                  'DstBinding-targets': 'ipv4if2',
                  'AffiliationStreamBlockLoadProfile.Load': 100}
        ret = {'tag': 'Client traff-$item'}

        tags = tM.getPoppedTags(params)
        val = params.get('tag')

        assert val == None
        assert tags == ret

    def test2b(self):
        tM = self.createTagManager()

        params = {'under': 'project1',
                  'EnableStreamOnlyGeneration': True,
                  'TrafficPattern': 'MESH',
                  'SrcBinding-targets': 'ipv4if1',
                  'DstBinding-targets': 'ipv4if2',
                  'AffiliationStreamBlockLoadProfile.Load': 100}
        ret = {}

        tags = tM.getPoppedTags(params)

        assert tags == ret
