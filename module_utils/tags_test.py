from module_utils.metamodel import MetaModel
from module_utils.datamodel import DataModel
from module_utils.xpath import NodeSelector, Linker, Selector
from module_utils.tags import TagManager

import pytest


class RestMock:

    def __init__(self):
        self.count = 0

    def create(self, obj, props):

        self.count = self.count + 1
        return obj + "-" + str(self.count)

    def get(self, obj, props=""):

        if obj == "tags1":
            return {"children": "tag1 tag2"}
        if obj == "tag1":
            return {"Name": "ABC-1"}
        if obj == "tag2":
            return {"Name": "ABC-2"}


class TestTag:

    def createModel(self):

        self.dm = DataModel()
        self.dm.new("dummy-session", [], [])

        self.root = project1 = self.dm.insert("project1", {"object_type": "project"})
        self.tags = self.dm.insert("tags1", {"object_type": "tags"}, project1)

        self.port1 = self.dm.insert("port1", {"object_type": "port", "name": "port1"}, project1)
        self.port2 = self.dm.insert("port2", {"object_type": "port", "name": "port2"}, project1)

        self.dev1 = self.dm.insert("emulateddevice1", {"object_type": "emulateddevice", "name": "dev1"}, self.port1)
        self.dev2 = self.dm.insert("emulateddevice2", {"object_type": "emulateddevice", "name": "dev2"}, self.port2)

        self.mm = MetaModel()
        self.mm.rest = RestMock()
        self.mm.datamodel = self.dm

    def test1(self):
        self.createModel()

        params = {'action': 'create', 'under': '/Project', 'objects': {}}
        params['objects'] = [{
            'EmulatedDevice': {
                'AffiliatedPort': "ref:/port[@name='Port1']",
                'name': 'BGPRouter 1',
                'tag': 'ctag'
            }
        }, {
            'EmulatedDevice': {
                'AffiliatedPort': "ref:/port[@name='Port1']",
                'name': 'BGPRouter 2',
                'tag': 'btag'
            }
        }]
        tagm = TagManager(self.mm)
        tags = tagm.update(params['objects'])
        assert params["objects"][0]["EmulatedDevice"]["usertag-targets"] == "tag-1"
        assert params["objects"][1]["EmulatedDevice"]["usertag-targets"] == "tag-2"
        assert len(tags) == 2

    def test2(self):
        self.createModel()

        params = {'action': 'create', 'under': '/Project', 'objects': {}}
        params['objects'] = {
            'EmulatedDevice': {
                'AffiliatedPort': "ref:/port[@name='Port1']",
                'name': 'BGPRouter 1',
                'tag': 'atag btag'
            }
        }
        tagm = TagManager(self.mm)
        tags = tagm.update(params['objects'])
        assert params["objects"]["EmulatedDevice"]["usertag-targets"] == "tag-1 tag-2"
        assert len(tags) == 2

    def test3(self):
        self.createModel()

        params = {'action': 'create', 'under': '/Project', 'objects': {}}
        params['objects'] = [{
            'EmulatedDevice': {
                'AffiliatedPort': "ref:/port[@name='Port1']",
                'name': 'BGPRouter 1',
                'tag': 'btag'
            }
        }, {
            'EmulatedDevice': {
                'AffiliatedPort': "ref:/port[@name='Port1']",
                'name': 'BGPRouter 2',
                'tag': 'btag'
            }
        }]

        tagm = TagManager(self.mm)
        tags = tagm.update(params['objects'])
        assert params["objects"][0]["EmulatedDevice"]["usertag-targets"] == "tag-1"
        assert params["objects"][1]["EmulatedDevice"]["usertag-targets"] == "tag-1"
        assert len(tags) == 1
