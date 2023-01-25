"""Logging system"""

import logging
import logging.config
from os import environ
from pathlib import Path
from threading import Lock

here = Path(__file__).absolute().parent
default_config_file = here / 'log.ini'
env_key = 'NLP_LOG_CONFIG_FILE'

_lock = Lock()
_configured = False
config_port = 9292


# Disallow using of logging system before it's configured
def _unintialized(*args, **kw):
    raise RuntimeError('logging system not configured')


debug = info = warning = error = fatal = exception = get_logger = _unintialized


def setup(config_file=None):
    """Setup configuration system from a config file (.ini format)"""
    global _configured
    global debug, info, warning, error, fatal, exception, get_logger

    with _lock:
        if _configured:
            return

        if not config_file:
            config_file = environ.get(env_key, default_config_file)

        logging.config.fileConfig(config_file)

        # Set real functions
        debug = logging.debug
        info = logging.info
        warning = logging.warning
        error = logging.error
        fatal = logging.fatal
        exception = logging.exception
        get_logger = logging.getLogger

        port = int(environ.get('NLP_LOG_CONFIG_PORT', config_port))
        thread = logging.config.listen(port)
        thread.daemon = True
        thread.start()

        _configured = True


if __name__ == '__main__':
    import json
    import struct
    from argparse import ArgumentParser
    from socket import socket

    levels = ['debug', 'info', 'warning', 'error', 'fatal']

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('level', choices=levels, help='level to set')
    parser.add_argument('--host', help='application host', default='localhost')
    parser.add_argument(
        '--port', help='application log config port', default=config_port,
        type=int)
    args = parser.parse_args()

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'incremental': True,
        'loggers': {
            '': {  # '' is the root logger
                'level': args.level.upper(),
            },
        }
    }

    payload = json.dumps(config).encode('utf-8')
    with socket() as sock:
        sock.connect((args.host, args.port))
        sock.send(struct.pack('>L', len(payload)))
        sock.sendall(payload)
