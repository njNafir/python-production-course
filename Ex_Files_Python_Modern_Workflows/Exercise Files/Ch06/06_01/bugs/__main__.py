"""Command line tool for bugs application"""
from argparse import ArgumentParser
from os import environ

from bugs import checks, httpd


def start(args):
    httpd.start(args.host, args.port)


def health(args):
    if not checks.health(args.url, args.timeout):
        raise SystemExit(1)


default_host = environ.get('BUGS_HOST', 'localhost')
default_port = int(environ.get('BUGS_PORT', 8080))
default_url = f'http://{default_host}:{default_port}'


parser = ArgumentParser(prog='bugs', description=__doc__)
sub = parser.add_subparsers()

start_parser = sub.add_parser('start')
start_parser.add_argument(
    '--host', help='host to listen on', default=default_host)
start_parser.add_argument(
    '--port', help='port to listen on', type=int, default=default_port)
start_parser.set_defaults(func=start)

health_parser = sub.add_parser('health')
health_parser.add_argument(
    'url', help='server base url', default=default_url, nargs='?')
health_parser.add_argument(
    '--timeout', help='check timeout (seconds)', type=float, default=30)
health_parser.set_defaults(func=health)

args = parser.parse_args()
args.func(args)
