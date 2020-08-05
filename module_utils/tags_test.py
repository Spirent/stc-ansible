

from module_utils.metamodel import MetaModel
from module_utils.tags import TagManager
from module_utils.xpath import Linker
from module_utils.datamodel import DataModel

import pytest


class RestMock:

    def __init__(self):
        self.count = 10

    def create(self, object_type, props):

        self.count = self.count + 1
        return object_type + "-" + str(self.count)

    def children(self, handle):
        if handle == 'tags1':
            return ['tag1', 'tag2']
        else:
            return []

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

    def config(self, handle, params):

        if '$item' in params:
            return False

        return True

    def perform(self, command, params={}):
        if command == "DeviceCreate":
            return {
                "LoopbackIf": "false",
                "DeviceTags": "",
                "State": "COMPLETED",
                "ProgressCurrentValue": "0",
                "EndTime": "1596608498.64631",
                "ReturnList": "router1 router2",
                "Status": "Create Device (Router) is successful",
                "ParentList": "project1",
                "IfStack": "Ipv4If PppIf PppoeIf EthIIIf",
                "DeviceCount": "5",
                "CreateClassId": "",
                "Active": "true",
                "ProgressCancelled": "false",
                "parent": "system1",
                "IfCount": "1 1 1 1",
                "ElapsedTime": "3",
                "ProgressDisplayCounter": "true",
                "DeviceType": "Router",
                "ProgressStepsCount": "1",
                "ProgressCurrentStep": "1",
                "AffiliatedDevice": "",
                "CreateCount": "2",
                "name": "dev-$item",
                "ProgressCurrentStepName": "",
                "StartTime": "1596608498.64288",
                "ProgressMaxValue": "0",
                "DeviceRole": "",
                "Port": "port1" }

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

    def createMetaModel(self):
        mm = MetaModel("127.0.0.1")
        mm.datamodel = DataModel()

        mm.rest = RestMock()
        mm.xpath = Linker(mm.datamodel, mm.rest)
        mm.rest = RestMock()
        mm.tagMgr = TagManager(mm.rest)

        mm.datamodel.new("dummy-session", [], [])
        mm.datamodel.insert("project1", {"object_type": "project"})
        return mm

    def test_performConfig_1a(self):
        t = self.createMetaModel()

        command = 'DeviceCreate'
        props = {'ParentList': 'project1',
                 'CreateCount': 2,
                 'DeviceCount': 5,
                 'Port': "Port1",
                 'IfStack': 'Ipv4If PppIf PppoeIf EthIIIf',
                 'IfCount': '1 1 1 1',
                 'name': 'dev-$item',
                 'tag': 'devTagDhcp devtag-$item'}

        retVal = "Value: ['router1', 'router2']"

        ret = str(t.performConfig(command, props))
        print(ret, type(ret))
        assert ret == retVal