# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-18 10:08:41
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-13 16:19:18

from ansible.module_utils.basic import *
from ansible.module_utils.metamodel import MetaModel


def main():

    fields = {
        "action": {
            "required": True,
            "type": "str"
        },
        "count": {
            "required": False,
            "type": "int",
            "default": 1
        },

        #create
        "objects": {
            "required": False,
            "type": "list"
        },
        "under": {
            "required": False,
            "type": "str"
        },

        #config
        "properties": {
            "required": False,
            "type": "dict"
        },
        "object": {
            "required": False,
            "type": "str"
        },

        # new_session
        "user": {
            "required": False,
            "type": "str"
        },
        "name": {
            "required": False,
            "type": "str"
        },

        # perform
        "command": {
            "required": False,
            "type": "str"
        },

        # load
        "datamodel": {
            "required": False,
            "type": "str"
        },
    }

    module = AnsibleModule(argument_spec=fields, no_log=False)

    try:
        mm = MetaModel()
        result = mm.action(module.params)
        mm.serialize()
        module.exit_json(changed=False, meta=result)

    except Exception as error:
        print("Oooops...", error)
        module.fail_json(msg=error)
        return


if __name__ == '__main__':
    main()