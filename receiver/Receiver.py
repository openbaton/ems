__author__ = 'lto'

import time
import sys

import stomp

class EMSReceiver(stomp.ConnectionListener):

    def __init__(self, orch_ip="localhost", orch_port="61613"):
        self.orch_ip = orch_ip
        self.orch_port = orch_port

    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)

        resp = "ak"
        conn = stomp.Connection(host_and_ports=self.orch_ip + ":" + self.orch_port)
        conn.send(body=resp, destination='/queue/ems-vnfm-actions')

