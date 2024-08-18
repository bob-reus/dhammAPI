from flask import Flask
from dhammapi.v1 import v1


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "This is the root page of DhammAPI. For information and usage, please visit https://www.github.com/bob-reus/dhammapi."

    app.register_blueprint(v1, url_prefix='/')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
