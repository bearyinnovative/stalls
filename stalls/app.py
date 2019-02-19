# -*- coding: utf-8 -*-

from envcfg.raw import stalls as config
from flask import Flask
from werkzeug.utils import import_string

from stalls.extensions import db


blueprints = [
    'stalls.modules.poll.api:bp',
]


def create_app(import_name=None):
    app = Flask(import_name or __name__)

    app.config.from_object('envcfg.raw.stalls')
    app.debug = bool(int(config.DEBUG))

    db.init_app(app)

    for bp_import_name in blueprints:
        bp = import_string(bp_import_name)
        app.register_blueprint(bp)

    return app
