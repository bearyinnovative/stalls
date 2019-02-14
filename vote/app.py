# -*- coding: utf-8 -*-

from envcfg.raw import vote as config
from flask import Flask
from werkzeug.utils import import_string

from vote.extensions import redis


blueprints = []


def create_app(import_name=None):
    app = Flask(import_name or __name__)

    app.config.from_object('envcfg.raw.vote')
    app.debug = bool(int(config.DEBUG))

    redis.init_app(app)

    for bp_import_name in blueprints:
        bp = import_string(bp_import_name)
        app.register_blueprint(bp)

    return app
