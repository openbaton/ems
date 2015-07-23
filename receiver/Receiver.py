import json
import logging
import subprocess

__author__ = 'lto'

import stomp

log = logging.getLogger(__name__)

class EMSReceiver(stomp.ConnectionListener):

    def __init__(self, conn):
        self.conn = conn
        self.scripts = True

    def on_error(self, headers, message):
        log.info('received an error %s' % message)

    def on_message(self, headers, message):
        if self.scripts:
            f = open("/opt/")

            self.scripts = False
        else:
            log.info('received a message %s' % message)
            proc = subprocess.Popen(message.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status = proc.wait()
            out, err = proc.communicate()


            resp = {
                'output': out,
                'err': err,
                'status': status
            }
            json_str = json.dumps(resp)
            log.info("answer is: " + json_str)
            self.conn.send(body=json_str, destination='/queue/ems-vnfm-actions')

