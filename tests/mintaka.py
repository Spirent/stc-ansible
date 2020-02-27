# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2019-03-05 08:49:39
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-14 14:31:28

import requests, json

class MintakaConfig:

    def __init__(self, host, version):

        url = 'http://mintaka.bdc.spirentcom.com/registry/servers'
        try:
            req = requests.get(url)
        except Exception as e:
            raise Exception('Sorry, failed to get configuration from Mintaka: %s' % to_native(e))

        servers = req.json()["result"]
        servers.sort(key=lambda x: x["ip"])

        self.stcv = []
        self.labserver = None
        for server in servers:
            if server["info"]["host"] == host and server["info"]["version"].startswith(version):

                if server["info"]["node"] == "stcv":
                    self.stcv.append(server)

                if server["info"]["node"] == "labserver":
                    self.labserver = server["ip"]

        if self.labserver == None:
            raise Exception('There is no lab-server available with version "%s"...' % version)

    def getLabServer(self):
        return self.labserver

    def getPorts(self, count=2):
        # Make sure the ports have the same hostip

        hostips = {}
        for i, stcv in enumerate(self.stcv):
            hostip = stcv["info"]["hostip"]
            if not (hostip in hostips):
                hostips[hostip] = []
            hostips[hostip].append(i)

        for hostip in hostips:

            if len(hostips[hostip]) >= count:

                l = []
                for i in range(0, count):
                    i1 = hostips[hostip][i]
                    l.append(self.stcv[i1]["ip"])

                return l

        raise Exception('There are no host with at least %d VMs' % count)

    def getPortsStr(self, count=2):
        mylist = self.getPorts(count)
        str = " ".join(mylist)
        return str


try:
    import os
    import re
    from ansible.plugins.vars import BaseVarsPlugin
    from ansible.module_utils._text import to_native
    from ansible.inventory.host import Host

    class VarsModule(BaseVarsPlugin):

        def get_vars(self, loader, path, entities, cache=True):
            ''' parses the inventory file '''

            if not isinstance(entities, list):
                entities = [entities]

            super(VarsModule, self).get_vars(loader, path, entities)
        
            data = {}
            for entity in entities:
                if isinstance(entity, Host):
                    try:
                        config = MintakaConfig(re.sub(r'-.*', '', entity.name), "5")
                        labServer = config.getLabServer()
                        chassis = config.getPortsStr(2)
                        data['ansible_host'] = labServer
                        data['chassis'] = chassis
                    except Exception as e:
                        self._display.warning(to_native(e))
            
            return data
except ImportError:
    pass