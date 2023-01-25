from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status = HTTPStatus.OK
        if self.path == '/':
            msg = b"What's Up, Doc?\n"
        elif self.path == '/health':
            msg = b'OK\n'
        else:
            status = HTTPStatus.NOT_FOUND
            msg = b''

        self.send_response(status)
        self.end_headers()
        self.wfile.write(msg)


def start(host, port):
    addr = (host, port)
    server = ThreadingHTTPServer(addr, Handler)
    logging.info('server ready on http://%s:%d', host, port)
    server.serve_forever()
