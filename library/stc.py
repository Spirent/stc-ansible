# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-18 10:08:41
# @Last Modified by:   rjezequel
# @Last Modified time: 2019-12-20 13:16:26

from ansible.module_utils.basic import *

from ansible.module_utils.metamodel import MetaModel



def main():

    fields = {
        "action": {"required": True, "type": "str"},

        #create
        "objects": {"required": False, "type": "list"},
        "under": {"required": False, "type": "str"},

        #config
        "properties": {"required": False, "type": "dict"},
        "parent": {"required": False, "type": "str"},

        # new_session
        "user": {"required": False, "type": "str"},
        "name": {"required": False, "type": "str"}
        
    }

    module = AnsibleModule(argument_spec=fields, no_log=False)

    try:
        error = None
        result= None
        mm = MetaModel()

        action = module.params["action"];
        if action == "new_session":

            mm.new_session(module.params["user"],module.params["name"])

        elif action == "create":

            mm.create(module.params["objects"],module.params["under"])

        elif action == "config":

            mm.config(module.params["properties"],module.params["parent"])

        else:

            raise Exception("Unknown action "+action)

        mm.serialize()

    except Exception as error:
        print("Oooops...",error)
        module.fail_json(msg=error, meta="nope")

    print("All fine!")
    module.exit_json(changed=False, meta="ok")


if __name__ == '__main__':
    main()