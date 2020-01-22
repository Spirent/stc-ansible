# -*- coding: utf-8 -*-
# @Author: rjezequel
# @Date:   2019-12-20 09:18:14
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-01-22 15:20:10

try:
    from ansible.module_utils.datamodel import DataModel
    from ansible.module_utils.logger import Logger
except ImportError:
    from module_utils.datamodel import DataModel
    from module_utils.logger import Logger

import requests
import pickle
import json
import re, fnmatch

log = Logger("stc-rest")


class StcRest:

    requests = []

    def __init__(self, server="127.0.0.1", session=""):
        self.server = server
        self.session = session
        self.errorInfo = None

    def new_session(self, user_name, session_name, reset_existing=True, kill_existing=False):

        url = "http://" + self.server + "/stcapi/system"
        systemInfo = json.loads(requests.get(url, headers={'Accept': 'application/json'}).content)
        log.info("SYSTEM %s -> %s" % (url, json.dumps(systemInfo, indent=4)))

        url = "http://" + self.server + "/stcapi/sessions"
        existingSessions = json.loads(requests.get(url, headers={'Accept': 'application/json'}).content)
        log.info("SESSIONS %s -> %s" % (url, json.dumps(existingSessions, indent=4)))

        newSession = True
        sessionID = session_name + " - " + user_name
        if sessionID in existingSessions:
            if kill_existing:
                log.info("Killing the session first")
                rsp = requests.delete(url + "/" + sessionID, headers={'Accept': 'application/json'}, params="kill")
                log.info("KILL SESSION -> [%d] %s" % (rsp.status_code, rsp.content))
            else:
                log.info("Session already exists... Skipping creation")
                newSession = False

        if newSession:
            log.info("Creating the session now...")
            params = {'userid': user_name, 'sessionname': session_name}
            rsp = requests.post(url, headers={'Accept': 'application/json'}, data=params, timeout=60 * 2)
            log.info("SESSION %s %s -> [%d] %s" % (url, json.dumps(params, indent=4), rsp.status_code, rsp.content))

            if rsp.status_code != 409 and rsp.status_code != 200 and rsp.status_code != 201:
                log.error("Failed to create a session: %s %s" % (rsp))
                return False

        self.session = sessionID
        if reset_existing and newSession and not self.perform("ResetConfig"):
            log.error("SESSION: failed to reset the session")
            return False

        version = self.get("system1", ["Version"])
        log.info("SERVER VERSION: %s" % version)
        return True

    def files(self):
        return self._get("files")

    def download(self, filename, destination="/tmp"):

        filename = fnmatch.translate(filename)

        files = []
        for file in self.files():

            if not re.match(filename, file):
                log.info("file %s does not match %s " % (file, filename))
                continue

            url = "http://" + self.server + "/stcapi/files/" + file
            rsp = requests.get(url,
                               headers={
                                   'Accept': 'application/octet-stream',
                                   "X-STC-API-Session": self.session
                               },
                               timeout=300)
            log.info("FILE %s -> [%d] %d bytes" % (url, rsp.status_code, len(rsp.content)))
            if rsp.status_code != 200:
                self.errorInfo = "download failed\n - url:%s\n - code:%d\n - response:%s\n - session:%s" % (
                    url, rsp.status_code, rsp.content, self.session)
                return None

            writenfile = destination + "/" + file
            with open(writenfile, 'wb') as f:
                f.write(rsp.content)
            log.info("Downloaded file written to %s " % writenfile)

            files.append(file)

        if len(files) == 0:
            self.errorInfo = "no files matching %s" % (filename)

        return files

    def connect(self, chassis_list):
        params = {chassis: True for chassis in chassis_list}
        params['action'] = 'connect'
        result = self._post("connections", params)
        return result != None

    def get(self, handle, properties=[]):
        container = "objects/" + handle
        if len(properties) > 0:
            container = container + "?" + (",".join(properties))
        response = self._get(container)
        if response == None:
            raise Exception(self.errorInfo)
        return response

    def children(self, handle, properties=[]):
        l = self.get(handle, ["children"])
        if l == None or l == '':
            return []
        return l.split(" ")

    def config(self, handle, params):
        """ Creates an object in the data moderl
        Parameters
        ----------
        handle :
            handle of the object to be configured
        params : 
            paramters of the object to be configured
        """
        url = "http://" + self.server + "/stcapi/objects/" + handle
        rsp = requests.put(url,
                           headers={
                               'Accept': 'application/json',
                               "X-STC-API-Session": self.session
                           },
                           data=params,
                           timeout=60)

        if rsp.status_code == 200 or rsp.status_code == 204:
            self.errorInfo = None
            log.info("CONFIG %s %s -> %s" % (url, json.dumps(params, indent=4), rsp.content))
            return True

        self.errorInfo = "config failed\n - url:%s\n - code:%d\n - response:%s\n - params:%s\n - session:%s!" % (
            url, rsp.status_code, rsp.content, params, self.session)
        log.error("CONFIG " + self.errorInfo)
        return False

    def create(self, object_type, params={}):
        """ Creates an object in the data model
        Parameters
        ----------
        params : 
            paramters of the object to be created
        """
        params["object_type"] = object_type
        result = self._post("objects", params)
        if result == None or (not "handle" in result) or result["handle"] == None:
            # raise Exception("Failed to create object: " + self.errorInfo)
            return None
        return result["handle"]

    def perform(self, command, params={}):
        """ Performs a command in the data-model
        Parameters
        ----------
        command:
            name of the command to be executed
        params : 
            paramters of the object to be created
        """

        if not command.lower().endswith("command"):
            command = command + "Command"
        params["command"] = command
        res = self._post("perform", params)
        if res == None:
            return None
            # raise Exception(self.errorInfo)
        return res

    def delete(self, object_handle):
        """ Deletes an object from the data model
        Parameters
        ----------
        name : object_handle
            Handle of the object to be deleted
        """

        url = "http://" + self.server + "/stcapi/objects/" + object_handle
        log.info("DELETE %s" % (url))
        rsp = requests.delete(url,
                              headers={
                                  'Accept': 'application/json',
                                  "X-STC-API-Session": self.session
                              },
                              timeout=60)

        if rsp.status_code == 200 or rsp.status_code == 204:
            log.info("DELETE status_code: %d -> %s" % (rsp.status_code, rsp.content))
            self.errorInfo = None
            return True

        self.errorInfo = "delete failed\n - url:%s\n - code:%d\n - response:%s\n - session:%s!" % (
            url, rsp.status_code, rsp.content, self.session)

        log.error("DELETE " + self.errorInfo)
        return None

    def _post(self, container, params={}):
        url = "http://" + self.server + "/stcapi/" + container
        log.info("POST %s %s" % (url, json.dumps(params, indent=4)))
        rsp = requests.post(url,
                            headers={
                                'Accept': 'application/json',
                                "X-STC-API-Session": self.session
                            },
                            json=params,
                            timeout=60)

        if rsp.status_code == 200 or rsp.status_code == 201:
            self.errorInfo = None
            log.info("POST status_code: %d -> %s" % (rsp.status_code, json.dumps(rsp.json(), indent=4)))
            return rsp.json()

        self.errorInfo = "failed\n - url:%s\n - code:%d\n - response:%s\n - params:%s\n - session:%s!" % (
            url, rsp.status_code, rsp.content, params, self.session)
        log.error("POST " + self.errorInfo)
        return None

    def _get(self, container):
        url = "http://" + self.server + "/stcapi/" + container
        log.info("GET %s" % (url))
        rsp = requests.get(url, headers={'Accept': 'application/json', "X-STC-API-Session": self.session}, timeout=60)

        if rsp.status_code == 200:
            self.errorInfo = None
            log.info("GET status_code: %d -> %s" % (rsp.status_code, json.dumps(rsp.json(), indent=4)))
            return rsp.json()

        self.errorInfo = "failed - url:%s - code:%d - content:%s!" % (url, rsp.status_code, rsp.content)
        log.error("GET " + self.errorInfo)
        return None
