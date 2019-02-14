# -*- coding: utf-8 -*-

from flask import Flask

from vote.extensions import redis, setup_redis


def create_app(import_name=None):
    app = Flask(import_namei or __name__)

    setup_redis(app)

    return app
