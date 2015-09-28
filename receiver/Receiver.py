import base64
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

#SCRIPTS_PATH = "/opt/openbaton/scripts"


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
            path = dict_msg.get('script-path')
            if not os.path.exists(path):
                os.makedirs(path)
            name = dict_msg.get('name')
            script = base64.b64decode(payload)
            if path[-1] == "/":
                path_name = path + "/" + name
            else:
                path_name = path + name
            path_name = path + "/" + name
            f = open(path_name, "w")
            f.write(script)
            log.info("Written %s into %s" % (script, path_name))
            out = str(os.listdir(path))
            err = ""
            status = 0

        if action == 'CLONE_SCRIPTS':
            path = dict_msg.get('script-path')
            url = payload
            log.debug("Cloning into: %s" % url)
            try:
                Repo.clone_from(url, path)
            except GitCommandError as e:
                err = traceback.format_exc()
                status = e.status
                out = None
            else:
                out = str(os.listdir(path))
                err = ""
                status = 0
        elif action == "EXECUTE":

            payload = SCRIPTS_PATH + "/" + payload
            env = dict_msg.get('env')
            log.debug("Executing: %s with env %s" % (payload, env))
            if env is None or len(env) == 0:
                env = None
            else:
                env.update(os.environ)

            proc = subprocess.Popen(["/bin/bash"] + payload.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            status = proc.wait()

            out, err = proc.communicate()

        elif action == "SCRIPTS_UPDATE":
            url = payload
            try:
                Repo.pull(url, "/opt/openbaton/scripts/")
            except GitCommandError as e:
                err = traceback.format_exc()
                status = e.status
                out = None
            else:
                out = str(os.listdir(SCRIPTS_PATH))
                err = ""
                status = 0

        if out is None:
            out = ""
        if err is None:
            err = ""

        resp = {
            'output': out,
            'err': err,
            'status': status
        }
        json_str = json.dumps(resp)
        log.info("answer is: " + json_str)

        self.conn.send(body=json_str, destination='/queue/%s-vnfm-actions' % self.hostname)
