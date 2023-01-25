"""nlp HTTP server"""

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import log


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_host, client_port = self.client_address
        log.debug('request from %s:%d', client_host, client_port)
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write('OK\n'.encode('utf-8'))
        self.wfile.flush()


def main():
    log.setup()

    host, port = '0.0.0.0', 8080
    server = ThreadingHTTPServer((host, port), Handler)
    log.info('server ready on %s:%d', host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
