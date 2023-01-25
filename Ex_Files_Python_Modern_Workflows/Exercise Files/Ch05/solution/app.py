"""Errors metrics decorator"""

from functools import wraps
from sys import exc_info
import logging


def report_errors(fn):
    fn.num_errors = 0

    @wraps(fn)
    def wrapper(*args, **kw):
        try:
            return fn(*args, **kw)
        finally:
            _, error, _ = exc_info()
            if error is not None:
                fn.num_errors += 1
                logging.error(
                    '%s %d errors (%s)', fn.__name__, fn.num_errors, error)
    return wrapper


@report_errors
def div(a, b):
    print(f'div({a}, {b})')
    return a / b


if __name__ == '__main__':
    div(1, 2)
    try:
        div(1, 0)
    except ZeroDivisionError:
        pass
