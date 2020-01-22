# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-18 10:08:41
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-22 14:17:30

from ansible.module_utils.basic import *
from ansible.module_utils.logger import Logger
from ansible.module_utils.metamodel import MetaModel
import traceback


def main():

    log = Logger("main")

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

        # session
        "user": {
            "required": False,
            "type": "str"
        },
        "name": {
            "required": False,
            "type": "str"
        },
        "chassis": {
            "required": False,
            "type": "str"
        },
        "reset_existing": {
            "required": False,
            "type": "bool"
        },
        "kill_existing": {
            "required": False,
            "type": "bool"
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

        # wait
        "timeout": {
            "required": False,
            "type": "int"
        },

        # download
        "file": {
            "required": False,
            "type": "str"
        },
        "dest": {
            "required": False,
            "type": "str"
        },
    }

    module = AnsibleModule(argument_spec=fields, no_log=False)

    try:
        mm = MetaModel()
        result = mm.action(module.params)
        mm.serialize()

        if result.isError():

            try:
                model = mm.datamodel.tree()
            except:
                model = None

            module.fail_json(msg=str(result.err).split("\n"), logs=Logger.logs, model=model)

        else:
            module.exit_json(changed=True, result=result.val, logs=Logger.logs)

    except Exception as error:

        log.error("Exception %s" % error)
        module.fail_json(msg="Oh no! Exception thrown...",
                         result=str(error).split("\n"),
                         trace=traceback.format_exc().split("\n"),
                         logs=Logger.logs)
        return


if __name__ == '__main__':
    main()
