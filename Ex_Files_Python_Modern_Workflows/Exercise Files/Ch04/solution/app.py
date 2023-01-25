"""Logging to stderr"""
import logging
from sys import stderr

log_format = \
    '[%(asctime)s] %(name)s:%(levelname)s %(module)s:%(funcName)s %(message)s'


logging.basicConfig(
    stream=stderr,
    format=log_format,
    level=logging.INFO,
)


def hello():
    logging.info('Roses are red')


if __name__ == '__main__':
    hello()
