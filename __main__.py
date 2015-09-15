import argparse
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
    hostname = _map.get("hostname") #get the hostname
    queue_type = _map.get("type")
    hostname = _map.get("hostname")
    conn = stomp.Connection(host_and_ports=[(_map.get("orch_ip"), int(_map.get("orch_port")))])
    conn.set_listener('ems_receiver', EMSReceiver(conn=conn, hostname=hostname))
    conn.start()
    conn.connect()
    conn.send(body='{"hostname":"%s"}' % hostname,destination='/queue/ems-%s-register' % queue_type)
    conn.subscribe(destination='/queue/vnfm-%s-actions' % queue_type, id=1, ack='auto')
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        conn.disconnect()
        sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Template Module', usage=usage)
    parser.add_argument('-l', '--log-level',
                        help='possible values are [0, 1, 2, 3, 4] where 0 is the maximum and 4 is lowest')

    if len(sys.argv) > 1:
        args = vars(parser.parse_args(sys.argv[1:]))
        log_level = args.get('log_level')
        level = LEVELS.get(log_level)
        logging.basicConfig(level=level)
    else:
        logging.basicConfig(level=logging.INFO)
    main()
