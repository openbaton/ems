
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

import argparse
import os
import sys
import time
import pkg_resources
import logging
import stomp
import ConfigParser

from receiver.Receiver import EMSReceiver
from utils.Utils import get_map

__author__ = 'lto'

log = logging.getLogger(__name__)
usage = "\nThis is the template module for the platform Crenation"

LEVELS = {'0': logging.DEBUG,
          '1': logging.INFO,
          '2': logging.WARNING,
          '3': logging.ERROR,
          '4': logging.CRITICAL,
          }


def main():
    # config_file_name = pkg_resources.resource_filename('etc', '/etc/openbaton/ems/conf.properties')
    config_file_name = "/etc/openbaton/ems/conf.ini"
    # pass the name to debugger
    log.debug(config_file_name)
    config = ConfigParser.ConfigParser() #create parser object
    config.read(config_file_name) #read config file
    _map = get_map(section='ems', config=config) #get the data from map
    queue_type = _map.get("type") #get type of the queue
    hostname = _map.get("hostname") #get hostname of the machine
    conn = stomp.Connection(host_and_ports=[(_map.get("orch_ip"), int(_map.get("orch_port")))]) #connect to activemq server using STOMP
    conn.set_listener('ems_receiver', EMSReceiver(conn=conn, hostname=hostname)) #use receiver object as listener
    while True:
        try:
            conn.start()
            conn.connect()
            break
        except:
            print "Cannot connect. Retrying"
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                sys.exit(0)
    conn.send(body='{"hostname":"%s"}' % hostname,destination='/queue/ems-%s-register' % queue_type) #send the registration message
    conn.subscribe(destination='/queue/vnfm-%s-actions' % hostname, id=1, ack='auto') #start waiting for messages in the respective queue
    print "EMS has connected to the destination queue"
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        conn.disconnect()
        sys.exit(0)


if __name__ == '__main__':
    logging_dir='/var/log/openbaton/'
    parser = argparse.ArgumentParser(description='Template Module', usage=usage)
    parser.add_argument('-l', '--log-level',
                        help='possible values are [0, 1, 2, 3, 4] where 0 is the maximum and 4 is lowest')

    if not os.path.exists(logging_dir):
    	os.makedirs(logging_dir)
    if len(sys.argv) > 1:
        args = vars(parser.parse_args(sys.argv[1:]))
        log_level = args.get('log_level')
        level = LEVELS.get(log_level)
        logging.basicConfig(filename=logging_dir+'/ems-receiver.log', level=level)
    else:
        logging.basicConfig(filename=logging_dir+'/ems-receiver.log', level=logging.DEBUG)
    main()
