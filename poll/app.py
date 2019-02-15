# -*- coding: utf-8 -*-

from envcfg.raw import applet_poll as config
from flask import Flask
from werkzeug.utils import import_string

from poll.extensions import db


blueprints = [
    'poll.modules.poll.api:bp',
]


def create_app(import_name=None):
    app = Flask(import_name or __name__)

    app.config.from_object('envcfg.raw.applet_poll')
    app.debug = bool(int(config.DEBUG))

    db.init_app(app)

    for bp_import_name in blueprints:
        bp = import_string(bp_import_name)
        app.register_blueprint(bp)

    return app
