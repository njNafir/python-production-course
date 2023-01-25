from datetime import datetime
from http import HTTPStatus
from os import environ

import pytz
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/current/<path:zone>')
def current(zone):
    try:
        tz = pytz.timezone(zone)
    except KeyError:
        resp = jsonify(error=f'unknown time zone - {zone}')
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp

    local = datetime.now().astimezone()
    time = local.astimezone(tz)

    return jsonify(time=time.isoformat())


def main():
    port = int(environ.get('TIMEZ_PORT')) or 8080
    app.run(
        host='0.0.0.0',
        port=port,
    )


if __name__ == '__main__':
    main()
