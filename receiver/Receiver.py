import json
import logging
import subprocess
import traceback
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

    def on_error(self, headers, message):
        log.info('received an error %s' % message)

    def on_message(self, headers, message):

        dict_msg = json.loads(message)

        action = dict_msg.get('action')
        log.info('received a message %s' % message)

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
                err = None
                status = 0
        elif action == "EXECUTE":
            payload = SCRIPTS_PATH + "/" + payload
            log.debug("Executing: " + payload)
            proc = subprocess.Popen(["sh"] + payload.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status = proc.wait()

            out, err = proc.communicate()

        resp = {
            'output': out,
            'err': err,
            'status': status
        }
        json_str = json.dumps(resp)
        log.info("answer is: " + json_str)

        self.conn.send(body=json_str, destination='/queue/%s-vnfm-actions' % self.hostname)
