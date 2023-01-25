from urllib.request import urlopen
from http import HTTPStatus


def health(base_url, timeout_sec):
    url = f'{base_url}/health'
    try:
        resp = urlopen(url, timeout=timeout_sec)
        return resp.code == HTTPStatus.OK
    except OSError:
        return False
