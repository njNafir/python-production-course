from . import __version__
from flask import Flask, jsonify
from socket import gethostname

app = Flask(__name__)
host = gethostname()


@app.route('/version')
def version():
    return jsonify(version=__version__, name='elmer', host=host)


if __name__ == '__main__':
    from os import environ
    app.run(
        host='0.0.0.0',
        port=int(environ.get('ELMER_PORT', 8080)),
        debug='ELMER_DEBUG' in environ,
    )
