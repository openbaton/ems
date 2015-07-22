import argparse
import sys
import time
import pkg_resources
import logging
import stomp
from receiver.Receiver import EMSReceiver

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
    config_file_name = pkg_resources.resource_filename('etc', 'config.ini')
    conn = stomp.Connection()
    conn.set_listener('', EMSReceiver())
    conn.start()
    conn.connect()

    conn.subscribe(destination='/queue/vnfm-ems-actions', id=1, ack='auto')

    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
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
