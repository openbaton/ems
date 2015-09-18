
 # Copyright (c) 2015 Fraunhofer FOKUS. All rights reserved.
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #     http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 #

import json
import logging
import subprocess
import traceback
from core.Managers import ConfigurationManager
from git import Repo, GitCommandError
import os

__author__ = 'lto'

import stomp

log = logging.getLogger(__name__)

SCRIPTS_PATH = "/opt/openbaton/scripts"


class EMSReceiver(stomp.ConnectionListener):
    def __init__(self, conn, hostname="generic"):
        self.conn = conn
        self.hostname = hostname
        self.configuration_manager = ConfigurationManager()

    def on_error(self, headers, message):
        log.info('received an error %s' % message)

    def on_message(self, headers, message):

        log.info('received a message: %s' % message)
        dict_msg = json.loads(message)

        action = dict_msg.get('action')

        payload = dict_msg.get('payload')

        if action == 'SAVE_SCRIPTS':
            if not os.path.exists(SCRIPTS_PATH):
                os.makedirs(SCRIPTS_PATH)
            url = payload
            log.debug("Cloning into: %s" % url)
            try:
                Repo.clone_from(url, "/opt/openbaton/scripts/")
            except GitCommandError as e:
                err = traceback.format_exc()
                status = e.status
                out = None
            else:
                out = str(os.listdir(SCRIPTS_PATH))
                err = ""
                status = 0
        elif action == "EXECUTE":

            payload = SCRIPTS_PATH + "/" + payload

            log.debug("Executing: " + payload)

            proc = subprocess.Popen(["sh"] + payload.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status = proc.wait()

            out, err = proc.communicate()

        elif action == "RUN":
            log.debug("Running: " + payload)
            proc = subprocess.Popen(payload.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            status = proc.wait()

            out, err = proc.communicate()

        elif action == "CONFIGURATION_UPDATE":
            res = {}
            for k, v in payload.iteritems():
                res[k] = str(self.configuration_manager.query(key=k))
                log.debug("key = %s, value = %s" % (k, res[k]))
            out = res
            err = ""
            status = 0


        resp = {
            'output': out,
            'err': err,
            'status': status
        }
        json_str = json.dumps(resp)
        log.info("answer is: " + json_str)

        self.conn.send(body=json_str, destination='/queue/%s-vnfm-actions' % self.hostname)
