"""Sample application"""

import logging
import logging.config

logging.config.fileConfig('log.ini')
logging.debug('the answer is %d', 42)
logging.critical('Please reinstall universe and reboot')
