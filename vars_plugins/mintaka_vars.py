# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2019-03-05 08:49:39
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-14 14:31:28

import re
import sys
sys.path.append('./tests/')
from mintaka import MintakaConfig
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